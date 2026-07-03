from __future__ import annotations

from chromadb.utils import embedding_functions

from backend.rag.config import DEFAULT_CONFIG, RagConfig


def get_embedding_function(config: RagConfig = DEFAULT_CONFIG):
    provider = config.embedding_provider.lower().strip()

    if provider in {"huggingface", "chroma-default", "onnx"}:
        return embedding_functions.DefaultEmbeddingFunction()

    if provider in {"sentence-transformers", "sentence_transformers"}:
        try:
            return embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=config.embedding_model_name,
            )
        except Exception as exc:
            raise RuntimeError(
                "Sentence Transformers embeddings require the sentence-transformers "
                "package. Install it or set MSME_RAG_EMBEDDING_PROVIDER=huggingface."
            ) from exc

    raise ValueError(
        "Unsupported embedding provider. Use 'huggingface' or 'sentence-transformers'."
    )
