import uuid
import json
from typing import Any, Dict, List, Optional

import faiss
import numpy as np
from pydantic import BaseModel, Field

from langchain_openai.embeddings import AzureOpenAIEmbeddings
from autogen_core.memory import Memory, MemoryContent, MemoryMimeType


def json_to_text(json_obj: Dict) -> str:
    result = []

    def flatten(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                flatten(v, f"{prefix}{k}: ")
        elif isinstance(obj, list):
            for idx, v in enumerate(obj):
                flatten(v, f"{prefix}[{idx}]: ")
        else:
            result.append(f"{prefix}{obj}")

    flatten(json_obj)
    return "\n".join(result)


class FAISSVectorMemoryConfig(BaseModel):
    """
    Configuration parameters for FAISS-based vector memory.
    """

    emb_model_name: str = Field(
        "text-embedding-3-large",
        description="Name of the embedding model to use.",
    )
    dimension: int = Field(..., description="Embedding dimension.")
    use_gpu: bool = Field(False, description="Use GPU if available.")
    top_k: int = Field(2, description="How many results to return on query.")
    score_threshold: float = Field(0.0, description="Minimum similarity score.")


class FAISSVectorMemory(Memory):
    """
    A simple example that uses an in-memory FAISS index to store embeddings and retrieve them.
    """

    def __init__(self, config: FAISSVectorMemoryConfig, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config = config
        self.dimension = self.config.dimension
        self.embeddings = AzureOpenAIEmbeddings(model=self.config.emb_model_name)

        # Create a FAISS index (flat L2, but customizable)
        self.index = faiss.IndexFlatL2(self.dimension)
        self.use_gpu = self.config.use_gpu

        self._embeddings: List[np.ndarray] = []
        self._documents: List[Dict[str, Any]] = []

        if self.use_gpu:
            # Move to GPU if supported
            res = faiss.StandardGpuResources()
            self.index = faiss.index_cpu_to_gpu(res, 0, self.index)

    def _get_embedding(self, text: str):
        return self.embeddings.embed_query(text)

    async def add(self, content: MemoryContent) -> None:
        """
        Add a single document/chunk to the FAISS index.
        """
        # Prepare embedding using the function defined elsewhere
        print("MIME type:", content.mime_type)

        if content.mime_type == MemoryMimeType.JSON:
            if isinstance(content.content, str):
                json_obj = json.loads(content.content)
            else:
                json_obj = content.content

            text_for_embedding = json_to_text(json_obj)
            embedding = self._get_embedding(text_for_embedding)
        else:
            embedding = self._get_embedding(content.content)

        embedding_np = np.array(embedding).astype("float32").reshape(1, -1)

        # Add to FAISS index
        self.index.add(embedding_np)

        # Store in local memory
        self._embeddings.append(embedding_np)
        self._documents.append(
            {
                "id": str(uuid.uuid4()),
                "content": content.content,
                "mime_type": content.mime_type,
                "metadata": content.metadata or {},
            }
        )

    async def query(self, input_query: MemoryContent) -> List[MemoryContent]:
        """
        Query FAISS for the most similar documents.
        """
        if not self._documents:
            return []

        # Compute query embedding using the function defined elsewhere
        query_embedding = self._get_embedding(input_query.content)
        query_embedding_np = np.array(query_embedding).astype("float32").reshape(1, -1)

        # Search in FAISS index
        distances, indices = self.index.search(query_embedding_np, self.config.top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue

            # Convert L2 distance to similarity score
            score = 1.0 / (1.0 + dist)
            if score < self.config.score_threshold:
                continue

            # Reconstruct matched document
            doc = self._documents[idx]
            results.append(
                MemoryContent(
                    content=doc["content"],
                    mime_type=doc["mime_type"],
                    metadata={**doc["metadata"], "score": float(score)},
                )
            )

        return results

    async def update_context(self, input_query: Any) -> None:
        """
        Update context based on matched documents.
        Extract `content` appropriately based on the context structure.
        """
        # Suppose context has an attribute `text` or similar; adjust as needed
        query_text = (
            input_query.get("text") if hasattr(input_query, "get") else str(input_query)
        )

        # Generate embedding from the extracted text content
        query_embedding = self._get_embedding(query_text)
        query_embedding_np = np.array(query_embedding).astype("float32").reshape(1, -1)

        # Search in FAISS index
        distances, indices = self.index.search(query_embedding_np, self.config.top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue

            score = 1.0 / (1.0 + dist)
            if score < self.config.score_threshold:
                continue

            doc = self._documents[idx]
            results.append(
                MemoryContent(
                    content=doc["content"],
                    mime_type=doc["mime_type"],
                    metadata={**doc["metadata"], "score": float(score)},
                )
            )

        # Output or handle matched contents as needed in your agent's context
        for mc in results:
            print(
                f"Matched chunk with score {mc.metadata.get('score')}:\n{mc.content}\n"
            )

    def dump_component(self) -> BaseModel:
        """
        Serialize the FAISS index to disk.
        """
        return self.config

    async def clear(self) -> None:
        """
        Clear all stored memory data.
        """
        self.index.reset()
        self._embeddings.clear()
        self._documents.clear()

    async def close(self):
        """
        Cleanup method if needed for persistence.
        """
        pass
