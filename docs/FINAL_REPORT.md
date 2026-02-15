# Project Report: CrediTrust RAG Complaint Chatbot

## 1. Objective

Build an internal AI-powered application to analyze CFPB customer complaints using Retrieval-Augmented Generation (RAG), enabling non-technical analysts to query the data and receive evidence-backed answers.

---

## 2. Task 1: Exploratory Data Analysis and Data Preprocessing

### EDA Findings

The exploratory data analysis revealed a significant volume of consumer complaints, with over 9.6 million records initially processed from the full CFPB dataset. Filtering for the target products and removing records without consumer narratives resulted in a massive dataset of over **1.37 million high-quality entries**. This scale ensures comprehensive coverage of consumer issues and historical trends.

Analysis of the product distribution showed that "Credit Card" and "Checking or savings account" complaints represent the largest segments, followed by "Personal Loans" and "Money transfers." This distribution highlights a diverse range of consumer friction points, from unauthorized charges to account access issues, necessitating a robust semantic search capability.

Narrative length analysis indicated that the majority of complaints range between 50 and 300 words. Very short narratives often lacked sufficient context for deep analysis, while exceptionally long narratives (some exceeding 1,000 words) justified the implementation of a recursive chunking strategy. Text cleaning (lowercasing, boilerplate removal, and normalization) successfully improved the signal-to-noise ratio, preparing the data for high-quality embedding generation.

---

## 3. Task 2: Text Chunking, Embedding, and Vector Store Indexing

### Sampling Strategy

To maximize organizational intelligence, the system successfully transitioned from a sampled environment to a full-scale deployment using **1,375,327 complaint records**. This was achieved by ingesting pre-computed embeddings provided in Parquet format, allowing the system to leverage high-volume data without the prohibitive computational cost of local embedding generation.

### Text Chunking

Complaint narratives were split using LangChain's `RecursiveCharacterTextSplitter` with the following parameters:

- **Chunk Size**: 500 characters
- **Chunk Overlap**: 50 characters

This choice ensures that each vector captures a focused semantic unit (about 2-3 sentences) while the overlap preserves context across boundaries, which is critical for maintaining coherence during retrieval.

### Embedding Model

We selected the `sentence-transformers/all-MiniLM-L6-v2` model. This model offers an excellent balance between performance and speed, generating high-quality 384-dimensional embeddings that are well-suited for both CPU-based inference and efficient similarity searches in FAISS.

---

## 4. Task 3: Building the RAG Core Logic and Evaluation

### Retrieval & Generation

The RAG pipeline implements a `Similarity Search` against the FAISS vector store, retrieving the **top-k=5** most relevant chunks for any given query. These chunks are then injected into a custom prompt template that instructs the LLM (FLAN-T5) to act as a CrediTrust analyst and answer using ONLY the provided evidence.

### Evaluation Results

The system was evaluated against 10 representative business questions. The qualitative results (including retrieved sources and generated answers) are documented in the [Evaluation Report](evaluation_report.md).

**Key Metrics:**

- **Questions Evaluated**: 10
- **Retrieval Rate**: 100% (sources found for all questions)
- **Average Sources per Question**: 5.0

---

## 5. Task 4: Creating an Interactive Chat Interface

### UI Features

The application features a professional Gradio-based web interface designed for internal analysts:

- **Intuitive Query Box**: Large text area for detailed question input.
- **Evidence Panel**: A dedicated section that displays the exact source complaint excerpts used to generate the answer, enhancing trust and auditability.
- **Smart Formatting**: Custom CSS ensures a clean, dashboard-like aesthetic with clear separation between the AI answer and supporting documentation.
- **Quick Links**: Example queries allow users to test common scenarios with a single click.

---

## 6. Conclusion

The CrediTrust RAG Complaint Chatbot successfully bridges the gap between raw unstructured data and actionable insights at a massive scale. By ingesting over 1.37 million records and optimizing for low-resource retrieval with a small but effective LLM, the system provides a robust tool for analyzing global consumer sentiment and identifying systemic risks across the financial portfolio.
