"""Execute curriculum notebooks that do not require an OpenAI API key."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"
NBCONVERT = [
    str(PYTHON),
    "-m",
    "jupyter",
    "nbconvert",
    "--to",
    "notebook",
    "--execute",
    "--inplace",
    "--ExecutePreprocessor.timeout=180",
    "--ExecutePreprocessor.kernel_name=python3",
]

OFFLINE = [
    ROOT / "notebooks/00_setup_and_python/00_python_for_coders.ipynb",
    ROOT / "notebooks/01_house_price/01_train_and_predict.ipynb",
    ROOT / "notebooks/02_sentiment/02_text_classify.ipynb",
    ROOT / "notebooks/03_rag_chatbot/03a_load_split_pdf.ipynb",
]


def run_nb(path: Path) -> None:
    print(f"\n=== EXECUTE {path.relative_to(ROOT)} ===")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    subprocess.run(NBCONVERT + [str(path)], check=True, cwd=str(path.parent), env=env)
    print("OK", path.name)


def check_api_imports() -> None:
    print("\n=== IMPORT CHECK (RAG modules) ===")
    code = """
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
print("RAG imports OK")
"""
    subprocess.run([str(PYTHON), "-c", code], check=True, cwd=str(ROOT))


def check_fastapi_model() -> None:
    print("\n=== FASTAPI MODEL FILE ===")
    model = ROOT / "data" / "sentiment_model.joblib"
    if not model.exists():
        raise SystemExit(f"Missing model after notebook 02: {model}")
    print("Found", model)


def main() -> None:
    if not PYTHON.exists():
        raise SystemExit("Missing .venv — create it first")
    for nb in OFFLINE:
        run_nb(nb)
    check_fastapi_model()
    check_api_imports()
    print("\nSMOKE PASS (offline notebooks + RAG imports)")
    print("Note: 03b/03c need OPENAI_API_KEY in .env — skipped here.")


if __name__ == "__main__":
    main()
