# rag_engine.py
# RAG Engine: Embeds knowledge base facts into FAISS, retrieves context for any ball event

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from knowledge_base import FACTS

class CricketRAGEngine:
    def __init__(self):
        print("Loading embedding model...")
        try:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:
            raise RuntimeError(
                f"Failed to load embedding model 'all-MiniLM-L6-v2': {e}\n"
                "Check your internet connection (first run downloads the model) "
                "or that 'sentence-transformers' is installed correctly."
            ) from e
        self.facts = list(FACTS)  # Start with static facts
        self.index = None
        self.embeddings = None
        self._build_index()

    def _build_index(self):
        """Embed all facts and build FAISS index."""
        print(f"Embedding {len(self.facts)} facts into FAISS...")
        self.embeddings = self.model.encode(self.facts, convert_to_numpy=True)
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)
        print(f"FAISS index built with {self.index.ntotal} vectors.")

    def add_live_fact(self, fact: str):
        """
        Dynamically add a new fact to the knowledge base during the match.
        This is the DYNAMIC LAYER — knowledge base grows ball by ball.
        """
        self.facts.append(fact)
        new_embedding = self.model.encode([fact], convert_to_numpy=True)
        self.index.add(new_embedding)
        print(f"  [RAG] Live fact added: {fact}")

    def retrieve(self, query: str, top_k: int = 4) -> list[str]:
        """
        Given a query (auto-generated from ball event),
        retrieve the top_k most relevant facts.
        """
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, top_k)
        results = [self.facts[i] for i in indices[0] if i < len(self.facts)]
        return results


if __name__ == "__main__":
    engine = CricketRAGEngine()

    # Test retrieval
    query = "Bumrah bowling to Tim Seifert, wicket"
    print(f"\nQuery: {query}")
    print("Retrieved context:")
    for fact in engine.retrieve(query):
        print(f"  - {fact}")

    # Test dynamic fact addition
    engine.add_live_fact("Bumrah has already taken 2 wickets in this innings today.")
    print("\nAfter live update:")
    for fact in engine.retrieve("Bumrah wickets today"):
        print(f"  - {fact}")