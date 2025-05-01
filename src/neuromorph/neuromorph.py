from neuromorph.agents.llm_backends.llm_backend import LLMBackend
from neuromorph.relationaldbs.database import Database
from neuromorph.vectordbs.vectorstore import VectorStore

from neuromorph.thinker import Thinker
from neuromorph.doer import Doer

class Neuromorph:
    def __init__(self, name: str = "Ada", llm_backend: LLMBackend = None, vector_db: VectorStore = None, relational_db: Database = None):
        self.name = name # TODO: add a StoredProc to add a core memory for name
        if llm_backend is None:
            raise ValueError("LLM backend must be provided.")
        if vector_db is None:
            raise ValueError("Vector database must be provided.")
        if relational_db is None:
            raise ValueError("Relational database must be provided.")
        self.thinker = Thinker(llm_backend=llm_backend, vector_db=vector_db, relational_db=relational_db)
