import typer
from typing import Optional
from rich.prompt import Prompt

from phi.agent import Agent
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.lancedb import LanceDb
from phi.vectordb.search import SearchType
from dotenv import load_dotenv

load_dotenv()

import os


def get_knowledge_base():
    vector_db = LanceDb(
        table_name="recipes",
        uri="/tmp/lancedb",
        search_type=SearchType.keyword,
    )

    pdf_knowledge_base = PDFKnowledgeBase(
    path="/Users/ashwjosh/AgentUniverse/ReActAgent/Phidata/IxNetworkManagerToolDemo/ixNetworkPDFs",
    # Table name: ai.pdf_documents
    vector_db=vector_db,
    reader=PDFReader(chunk=True),)
    # Comment out after first run

    pdf_knowledge_base.load(recreate=False)

    return pdf_knowledge_base