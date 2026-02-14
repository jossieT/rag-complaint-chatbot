# Project Report: CrediTrust RAG Complaint Chatbot

## 1. Objective

Build an internal AI-powered application to analyze CFPB customer complaints using Retrieval-Augmented Generation (RAG), enabling non-technical analysts to query the data and receive evidence-backed answers.

---

## 2. Task 1: Exploratory Data Analysis and Data Preprocessing

### EDA Findings

The exploratory data analysis revealed a significant volume of consumer complaints, with over 9.6 million records initially processed from the full CFPB dataset. Filtering for the five target products (Credit card, Personal loan, Savings account, and Money transfers) and removing records without consumer narratives resulted in a refined dataset of approximately 454,472 high-quality entries. This filtering ensured that the RAG system's knowledge base remains strictly relevant to the intended business domains.

Analysis of the product distribution showed that "Credit Card" and "Checking or savings account" complaints represent the largest segments, followed by "Personal Loans" and "Money transfers." This distribution highlights a diverse range of consumer friction points, from unauthorized charges to account access issues, necessitating a robust semantic search capability.

Narrative length analysis indicated that the majority of complaints range between 50 and 300 words. Very short narratives often lacked sufficient context for deep analysis, while exceptionally long narratives (some exceeding 1,000 words) justified the implementation of a recursive chunking strategy. Text cleaning (lowercasing, boilerplate removal, and normalization) successfully improved the signal-to-noise ratio, preparing the data for high-quality embedding generation.

---

## 3. Task 2: Text Chunking, Embedding, and Vector Store Indexing

### Sampling Strategy

To balance computational efficiency with representative coverage, a stratified sample of **15,000 complaints** was extracted from the cleaned dataset. Stratification was performed based on the `Product` category to ensure that even lower-volume products (like Money Transfers) are proportionally represented in the vector store, preventing the system from becoming biased toward high-volume categories like Credit Cards.

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

The CrediTrust RAG Complaint Chatbot successfully bridges the gap between raw unstructured data and actionable insights. By combining robust preprocessing, stratified sampling, and semantic retrieval, the system provides a powerful tool for analyzing consumer sentiment and identifying systemic issues in financial products.
