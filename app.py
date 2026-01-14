"""
Interactive Chat Interface for CrediTrust Financial Complaint Analysis

This application provides a web-based interface for non-technical users to:
- Ask questions about customer complaints
- Receive AI-generated answers grounded in retrieved data
- View source complaint excerpts for transparency
"""

import os
import logging
import gradio as gr
from src.rag_pipeline import RAGPipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize the RAG Pipeline
logger.info("Initializing RAG Pipeline for Chat Interface...")
try:
    rag = RAGPipeline()
except Exception as e:
    logger.error(f"Failed to initialize RAG Pipeline: {e}")
    rag = None

def chat_interface(question: str):
    """
    Function to handle user questions and return AI answers with sources.
    """
    if not question.strip():
        return "Please enter a valid question.", "No sources available."
    
    if rag is None:
        return "Error: RAG Pipeline not initialized. Please check logs.", "No sources available."
    
    try:
        # Query the RAG system
        logger.info(f"Processing question: {question}")
        response = rag.query(question)
        
        answer = response.get("answer", "I couldn't generate an answer.")
        sources_list = response.get("sources", [])
        
        # Format sources for display
        if not sources_list:
            sources_display = "No relevant complaint excerpts found for this query."
        else:
            sources_parts = []
            for i, source in enumerate(sources_list, 1):
                meta = source.get("metadata", {})
                excerpt = source.get("content", "N/A")
                
                source_text = f"""### Source {i}
- **Product Category:** {meta.get('product_category', 'N/A')}
- **Issue:** {meta.get('issue', 'N/A')}
- **Complaint ID:** {meta.get('complaint_id', 'N/A')}
- **Date Received:** {meta.get('date_received', 'N/A')}

**Complaint Excerpt:**
> {excerpt}
"""
                sources_parts.append(source_text)
            
            sources_display = "\n\n---\n\n".join(sources_parts)
            
        return answer, sources_display
        
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        return f"An error occurred: {str(e)}", "No sources available."

# Custom CSS for a professional look
custom_css = """
.container { max-width: 900px; margin: auto; padding: 20px; }
.header { text-align: center; margin-bottom: 30px; }
.sources-panel { background-color: #f9f9f9; border-left: 5px solid #007bff; padding: 15px; border-radius: 5px; }
"""

# Build the Gradio UI
with gr.Blocks(css=custom_css, title="CrediTrust Complaint Analyst") as demo:
    with gr.Column(elem_classes="container"):
        # Header Section
        gr.Markdown(
            """
            # 🏦 CrediTrust Financial Complaint Analyst
            ### Internal RAG System for Customer Insight
            
            Ask questions about customer complaints to get evidence-backed answers grounded in our complaint database.
            """,
            elem_classes="header"
        )
        
        with gr.Row():
            with gr.Column(scale=2):
                # Input Box
                input_box = gr.Textbox(
                    label="What would you like to know about our customer complaints?",
                    placeholder="e.g., Why are customers unhappy with Credit Cards?",
                    lines=3
                )
                
                with gr.Row():
                    submit_btn = gr.Button("🔍 Ask Assistant", variant="primary")
                    clear_btn = gr.Button("🗑️ Clear")
            
            with gr.Column(scale=3):
                # Output Area
                output_answer = gr.Markdown(label="AI-Generated Answer")
        
        # Sources Section
        gr.Markdown("## 📄 Supporting Evidence & Sources")
        with gr.Column(elem_classes="sources-panel"):
            output_sources = gr.Markdown(label="Retrieved Complaint Excerpts")
            
        # Event Handlers
        submit_btn.click(
            fn=chat_interface,
            inputs=input_box,
            outputs=[output_answer, output_sources]
        )
        
        clear_btn.click(
            fn=lambda: (None, None, None),
            inputs=None,
            outputs=[input_box, output_answer, output_sources]
        )
        
        # Example queries
        gr.Examples(
            examples=[
                ["Why are customers unhappy with Credit Cards?"],
                ["What recurring issues appear in Money Transfers?"],
                ["What are the main complaints about Personal Loans?"],
                ["How do customers describe fraudulent transactions?"]
            ],
            inputs=input_box
        )

# Launch the app
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
