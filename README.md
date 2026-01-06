# RAG Complaint Chatbot

An internal AI-powered application designed to analyze CFPB (Consumer Financial Protection Bureau) customer complaints using Retrieval-Augmented Generation (RAG). This project turns unstructured complaint data into actionable insights for financial internal teams.

## 🚀 Project Overview

The project is being developed in phases:

- **Task 1**: Data Preprocessing & Cleaning.
- **Task 2**: Text Chunking, Embedding generation, and Vector Store Indexing.
- **Task 3** (Planned): Retrieval & RAG Pipeline.
- **Task 4** (Planned): Deployment & User Interface.

## 🛠️ Installation & Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd rag-complaint-chatbot
```

### 2. Install Dependencies

```bash
pip install pandas scikit-learn langchain-text-splitters langchain-huggingface langchain-community faiss-cpu sentence-transformers
```

**Note for Windows Users**:
If you encounter `DLL initialization routine failed` errors, reinstall `torch` using the CPU-specific bundle:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu --force-reinstall
```

## 📂 Project Structure

```
rag-complaint-chatbot/
├── data/
│   ├── raw/             # Original CFPB dataset (CSV)
│   └── processed/       # Cleaned and filtered data
├── notebooks/           # Jupyter notebooks for EDA and testing
├── src/                 # Source code
│   ├── preprocessing.py         # Cleaning logic
│   ├── process_full_dataset.py  # Full pipeline execution
│   └── build_vector_store.py    # Chunking & Indexing
├── vector_store/        # Persisted FAISS index files
├── README.md
└── .gitignore           # Configured to ignore large data files
```

## 🔄 Core Pipeline

### Phase 1: Data Preprocessing

Executes broad cleaning on the 6GB+ CFPB dataset.

- **Filter**: Targets "Credit Cards", "Personal Loans", "Savings Accounts", and "Money Transfers".
- **Clean**: Lowercasing, removing boilerplate phrases, and stripping special characters.

**Run command:**

```bash
python src/process_full_dataset.py
```

### Phase 2: Vector Store Indexing

Transform text into a searchable semantic index.

- **Sampling**: Stratified sample of 15,000 complaints to maintain category proportions.
- **Chunking**: `RecursiveCharacterTextSplitter` (size: 500, overlap: 50).
- **Embedding**: `sentence-transformers/all-MiniLM-L6-v2`.
- **Indexing**: `FAISS` for high-performance similarity search.

**Run command:**

```bash
python src/build_vector_store.py
```

## 📝 Deliverables

- Cleaned dataset in `data/processed/`.
- Searchable vector store in `vector_store/`.
- Modular, documented Python scripts in `src/`.
