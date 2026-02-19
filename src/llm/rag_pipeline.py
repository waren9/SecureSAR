from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict

from opensearchpy import OpenSearch

from src.utils.config import load_config


@dataclass
class RAGPipeline:
    """
    Very lightweight RAG pipeline that retrieves SAR templates and regulatory
    text snippets from OpenSearch. For local development without OpenSearch,
    this will catch connection errors and return empty results.
    """

    def __post_init__(self) -> None:
        cfg = load_config()
        self.endpoint = cfg.opensearch.endpoint
        self.index = cfg.opensearch.sar_index
        # For simplicity, assume anonymous / dev auth; production should use IAM or basic auth.
        self.client = OpenSearch(
            hosts=[self.endpoint],
            use_ssl=self.endpoint.startswith("https"),
            verify_certs=False,
        )

    def retrieve_context(self, query: str, size: int = 5) -> List[Dict[str, str]]:
        """
        Retrieve top-N relevant documents for the given query.
        """
        try:
            resp = self.client.search(
                index=self.index,
                body={
                    "size": size,
                    "query": {"multi_match": {"query": query, "fields": ["title", "body"]}},
                },
            )
        except Exception:
            # Local/dev fallback when OpenSearch is unavailable
            return []

        hits = resp.get("hits", {}).get("hits", [])
        return [
            {
                "id": h.get("_id", ""),
                "title": h.get("_source", {}).get("title", ""),
                "body": h.get("_source", {}).get("body", ""),
            }
            for h in hits
        ]


__all__ = ["RAGPipeline"]

