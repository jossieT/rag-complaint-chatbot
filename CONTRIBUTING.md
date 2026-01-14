# Contributing to CrediTrust RAG Complaint Chatbot

Thank you for your interest in contributing! We welcome help in making this a better tool for financial analyst teams.

## Development Setup

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd rag-complaint-chatbot
   ```

2. **Environment**:
   Use Python 3.10+. It is highly recommended to use a virtual environment.

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   pip install flake8 pytest  # For development
   ```

4. **Configuration**:
   Copy or modify `config.yaml` to suit your local environment if necessary.

## Workflow

1. **Branching**: Create a feature branch for your changes.
   `git checkout -b feature/your-feature-name`
2. **Coding Standards**:
   - Follow PEP 8 style guidelines.
   - Run `flake8 .` before committing to check for linting issues.
3. **Testing**:
   - Add unit tests for new logic where possible.
   - Run `pytest` to ensure nothing is broken.
4. **Pull Requests**:
   - Provide a clear description of your changes.
   - Ensure the CI pipeline (GitHub Actions) passes.

## Project Structure

- `src/`: Core logic (preprocessing, indexing, RAG pipeline).
- `app.py`: Gradio web interface.
- `config.yaml`: Centralized system parameters.
- `docs/`: Documentation and evaluation reports.

## Questions?

Reach out to the project maintainers for help!
