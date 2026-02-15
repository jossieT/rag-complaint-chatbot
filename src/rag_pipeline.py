"""
RAG Pipeline for CrediTrust Financial Complaint Analysis

This module implements the core Retrieval-Augmented Generation (RAG) logic:
- Vector store loading
- Query retrieval
- Prompt engineering
- Answer generation with LLM
"""

import os
import logging
import yaml
from typing import List, Dict, Any, Tuple
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Complete RAG pipeline for complaint analysis.
    """
    
    def __init__(
        self, 
        config_path: str = "config.yaml"
    ):
        """
        Initialize the RAG pipeline.
        
        Args:
            config_path: Path to the configuration YAML file
        """
        self.config = self._load_config(config_path)
        self.vector_store_path = self.config['paths']['vector_store']
        self.embedding_model_name = self.config['models']['embeddings']
        self.llm_model_name = self.config['models']['llm']
        self.top_k = self.config['rag_params']['top_k']
        
        self.vector_store = None
        self.embeddings = None
        
        # Load vector store
        self._load_vector_store()

    def _load_config(self, config_path: str) -> Dict:
        """Load the configuration from YAML."""
        if not os.path.exists(config_path):
            # Fallback defaults if config missing
            return {
                'paths': {'vector_store': 'vector_store'},
                'models': {
                    'embeddings': 'sentence-transformers/all-MiniLM-L6-v2',
                    'llm': 'google/flan-t5-small'
                },
                'rag_params': {'top_k': 5, 'max_new_tokens': 200}
            }
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _load_vector_store(self):
        """Load the FAISS vector store and embedding model."""
        try:
            logger.info(f"Loading vector store from {self.vector_store_path}...")
            
            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model_name
            )
            
            # Load FAISS index
            self.vector_store = FAISS.load_local(
                self.vector_store_path,
                self.embeddings,
                allow_dangerous_deserialization=True  # Required for loading pickled data
            )
            
            logger.info("Vector store loaded successfully.")
            
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            raise
    
    def retrieve_relevant_complaints(
        self, 
        query: str, 
        k: int = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant complaint chunks for a given query.
        
        Args:
            query: User's question
            k: Number of documents to retrieve (defaults to self.top_k)
            
        Returns:
            List of dictionaries containing document content and metadata
        """
        if k is None:
            k = self.top_k
            
        try:
            logger.info(f"Retrieving top {k} documents for query: '{query[:50]}...'")
            
            # Perform similarity search
            docs_with_scores = self.vector_store.similarity_search_with_score(
                query, 
                k=k
            )
            
            # Format results
            results = []
            for doc, score in docs_with_scores:
                result = {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": float(score)
                }
                results.append(result)
            
            logger.info(f"Retrieved {len(results)} documents.")
            return results
            
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return []
    
    def _format_context(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """
        Format retrieved documents into a context string for the LLM.
        
        Args:
            retrieved_docs: List of retrieved document dictionaries
            
        Returns:
            Formatted context string
        """
        if not retrieved_docs:
            return "No relevant complaint data found."
        
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            content = doc["content"]
            # Simplified metadata for the model
            category = doc["metadata"].get('product_category', 'N/A')
            issue = doc["metadata"].get('issue', 'N/A')
            
            context_part = f"Source {i} (Product: {category}, Issue: {issue}): {content}"
            context_parts.append(context_part)
        
        return "\n\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """
        Create the prompt for the LLM.
        """
        # Prioritize the question and instructions in case of truncation
        prompt = f"""QUESTION: {query}
        
ANSWER THE ABOVE QUESTION USING THESE COMPLAINT EXCERPTS:
{context[:1500]}  # Hard limit to prevent total truncation

If the answer is not in the excerpts, say "Information not available."
"""
        return prompt
    
    def generate_answer(
        self, 
        query: str, 
        use_huggingface: bool = True,
        model_name: str = None
    ) -> Dict[str, Any]:
        """
        Generate an answer using the RAG pipeline.
        
        Args:
            query: User's question
            use_huggingface: Whether to use HuggingFace inference
            model_name: Name of the LLM to use (defaults to self.llm_model_name)
            
        Returns:
            Dictionary containing answer and source documents
        """
        if model_name is None:
            model_name = self.llm_model_name
        try:
            # Step 1: Retrieve relevant documents
            retrieved_docs = self.retrieve_relevant_complaints(query)
            
            if not retrieved_docs:
                return {
                    "answer": "I couldn't find any relevant complaint data to answer your question.",
                    "sources": [],
                    "query": query
                }
            
            # Step 2: Format context
            context = self._format_context(retrieved_docs)
            
            # Step 3: Create prompt
            prompt = self._create_prompt(query, context)
            
            # Step 4: Generate answer
            if use_huggingface:
                answer = self._generate_with_huggingface(prompt, model_name)
            else:
                # Fallback: Use a simple extractive approach
                answer = self._generate_extractive_answer(query, retrieved_docs)
            
            # Step 5: Return structured response
            return {
                "answer": answer,
                "sources": retrieved_docs[:2],  # Return top 2 sources for display
                "query": query,
                "num_sources": len(retrieved_docs)
            }
            
        except Exception as e:
            logger.error(f"Answer generation failed: {e}")
            return {
                "answer": f"An error occurred while generating the answer: {str(e)}",
                "sources": [],
                "query": query
            }
    
    def _generate_with_huggingface(self, prompt: str, model_name: str) -> str:
        """
        Generate answer using HuggingFace inference.
        
        Args:
            prompt: Complete prompt
            model_name: HuggingFace model name
            
        Returns:
            Generated answer
        """
        try:
            from transformers import pipeline
            
            logger.info(f"Generating answer with {model_name}...")
            
            # Initialize the pipeline
            generator = pipeline(
                "text2text-generation",
                model=model_name,
                max_length=512,
                device=-1  # CPU
            )
            
            # Generate
            result = generator(prompt, max_new_tokens=200, do_sample=False)
            answer = result[0]["generated_text"]
            
            return answer.strip()
            
        except Exception as e:
            logger.warning(f"HuggingFace generation failed: {e}. Falling back to extractive method.")
            return self._generate_extractive_answer(prompt.split("Question:")[-1].split("Answer:")[0].strip(), [])
    
    def _generate_extractive_answer(
        self, 
        query: str, 
        retrieved_docs: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a simple extractive answer by summarizing retrieved documents.
        This is a fallback method when LLM generation fails.
        
        Args:
            query: User's question
            retrieved_docs: Retrieved documents
            
        Returns:
            Extractive answer
        """
        if not retrieved_docs:
            return "No relevant complaint data found to answer this question."
        
        # Extract key information
        products = set()
        issues = set()
        
        for doc in retrieved_docs:
            metadata = doc["metadata"]
            if metadata.get("product_category"):
                products.add(metadata["product_category"])
            if metadata.get("issue"):
                issues.add(metadata["issue"])
        
        # Create a simple summary
        answer_parts = []
        
        if products:
            answer_parts.append(f"Based on the retrieved complaints, the main products involved are: {', '.join(products)}.")
        
        if issues:
            answer_parts.append(f"The primary issues reported include: {', '.join(list(issues)[:3])}.")
        
        answer_parts.append(f"This analysis is based on {len(retrieved_docs)} relevant complaint(s).")
        
        return " ".join(answer_parts)
    
    def query(self, user_question: str) -> Dict[str, Any]:
        """
        Main entry point for querying the RAG system.
        
        Args:
            user_question: User's question
            
        Returns:
            Complete response with answer and sources
        """
        if not user_question or not isinstance(user_question, str):
            logger.warning("Invalid or empty user question provided.")
            return {
                "answer": "Please provide a valid question.",
                "sources": [],
                "query": ""
            }
        return self.generate_answer(user_question)


def main():
    """Test the RAG pipeline with sample queries."""
    logger.info("=" * 80)
    logger.info("RAG Pipeline Test")
    logger.info("=" * 80)
    
    # Initialize pipeline
    try:
        rag = RAGPipeline()
    except Exception as e:
        logger.error(f"Failed to initialize RAG pipeline: {e}")
        return
    
    # Test queries
    test_queries = [
        "Why are customers unhappy with Credit Cards?",
        "What are the main issues with Money Transfers?",
        "What problems do customers face with Personal Loans?"
    ]
    
    for query in test_queries:
        logger.info(f"\n{'=' * 80}")
        logger.info(f"Query: {query}")
        logger.info(f"{'=' * 80}")
        
        response = rag.query(query)
        
        logger.info(f"\nAnswer: {response['answer']}")
        logger.info(f"\nNumber of sources: {response['num_sources']}")
        
        if response['sources']:
            logger.info("\nTop Sources:")
            for i, source in enumerate(response['sources'], 1):
                logger.info(f"\n--- Source {i} ---")
                logger.info(f"Product: {source['metadata'].get('product_category', 'N/A')}")
                logger.info(f"Issue: {source['metadata'].get('issue', 'N/A')}")
                logger.info(f"Excerpt: {source['content'][:200]}...")
    
    logger.info(f"\n{'=' * 80}")
    logger.info("Test Complete!")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
