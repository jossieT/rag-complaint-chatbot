import os
import logging
import gradio as gr
import yaml
from src.rag_pipeline import RAGPipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize the RAG Pipeline
logger.info("Initializing Intelligence Engine...")
try:
    rag = RAGPipeline()
except Exception as e:
    logger.error(f"Failed to initialize Intelligence Engine: {e}")
    rag = None

def analyze_query(question: str):
    """
    Handle analytical queries and return formatted intelligence with source evidence.
    """
    if not question.strip():
        return "Warning: Please provide a valid analytical query.", ""
    
    if rag is None:
        return "Internal Error: Intelligence Engine offline. Contact system administrator.", ""
    
    try:
        logger.info(f"Processing analytical query: {question}")
        response = rag.query(question)
        
        answer = response.get("answer", "Analysis inconclusive based on available data.")
        sources_list = response.get("sources", [])
        
        # Format sources for professional display
        if not sources_list:
            sources_display = "_No corroborating evidence found in the primary database for this specific query._"
        else:
            sources_parts = []
            for i, source in enumerate(sources_list, 1):
                meta = source.get("metadata", {})
                excerpt = source.get("content", "N/A")
                
                source_text = f"""### Evidence Record {i}
- **Category:** {meta.get('product_category', 'N/A')}
- **Specific Issue:** {meta.get('issue', 'N/A')}
- **Reference ID:** {meta.get('complaint_id', 'N/A')}
- **Filing Date:** {meta.get('date_received', 'N/A')}

**Case Excerpt:**
> {excerpt}
"""
                sources_parts.append(source_text)
            
            sources_display = "\n\n---\n\n".join(sources_parts)
            
        return answer, sources_display
        
    except Exception as e:
        logger.error(f"Intelligence generation failed: {e}")
        return f"System Failure: {str(e)}", ""

# Professional Financial Theme CSS
custom_css = """
body { background-color: #f4f7f9; }
.gradio-container { font-family: 'Inter', -apple-system, sans-serif !important; }
.header-text { text-align: left; border-bottom: 2px solid #2d3e50; padding-bottom: 10px; margin-bottom: 20px; }
.sidebar { background-color: #ffffff; border-right: 1px solid #e1e8ed; padding: 20px; border-radius: 8px; }
.main-panel { padding: 20px; }
.footer-note { font-size: 0.85em; color: #64748b; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 10px; }
.evidence-panel { background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 15px; }
button.primary { background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important; border: none !important; }
button.primary:hover { opacity: 0.9; }
"""

# Build the Intelligence Dashboard
with gr.Blocks(title="CrediTrust Intelligence Dashboard") as demo:
    with gr.Row():
        # Sidebar for Context and Examples
        with gr.Column(scale=1, elem_classes="sidebar") as sidebar:
            gr.Markdown(
                """
                # 🏦 CrediTrust
                **Intelligence Dashboard**
                v1.2.0-Alpha
                
                ---
                ### 🛠️ Analytical Toolkit
                This interface utilizes Retrieval-Augmented Generation (RAG) to provide grounded insights from the CFPB complaint database.
                """
            )
            
            # Examples will be added here later after query_input is defined
            
            gr.Markdown(
                """
                ---
                ### ⚖️ Compliance Notice
                *This tool provides AI-generated analysis based on internal datasets. Findings should be cross-referenced with original filings for final auditing.*
                """,
                elem_classes="footer-note"
            )

        # Main Analytical Panel
        with gr.Column(scale=3, elem_classes="main-panel"):
            gr.Markdown(
                """
                # Executive Analysis Console
                *Submit natural language queries to extract intelligence from over 450,000 processed consumer filings.*
                """,
                elem_classes="header-text"
            )
            
            with gr.Group():
                query_input = gr.Textbox(
                    label="Analytical Query Input",
                    placeholder="Enter your inquiry regarding consumer complaint patterns...",
                    lines=3,
                    interactive=True
                )
                
                with gr.Row():
                    submit_btn = gr.Button("🚀 Execute Analysis", variant="primary")
                    clear_btn = gr.Button("🔄 Reset Terminal")

            # Now add examples to the sidebar since query_input is defined
            with sidebar:
                gr.Markdown("### 📌 Example Queries")
                gr.Examples(
                    examples=[
                        ["Identify primary friction points in Credit Card services."],
                        ["Analyze recurring issues within Money Transfer protocols."],
                        ["Summarize customer sentiment regarding Personal Loan interest disclosures."],
                        ["Evaluate common obstacles in Savings Account access."],
                        ["Describe the profile of reported fraudulent transactions."]
                    ],
                    inputs=[query_input],
                    label=""
                )

            gr.Markdown("## 📋 Executive Summary & Analysis")
            output_answer = gr.Markdown(label="Intelligence Report")
            
            with gr.Accordion("🔍 Supporting Evidence & Case Excerpts", open=False):
                output_sources = gr.Markdown(elem_classes="evidence-panel")

    # Event Handlers
    submit_btn.click(
        fn=analyze_query,
        inputs=query_input,
        outputs=[output_answer, output_sources],
        show_progress="full"
    )
    
    clear_btn.click(
        fn=lambda: ("", "", ""),
        inputs=None,
        outputs=[query_input, output_answer, output_sources]
    )

# Dashboard Deployment Configuration
if __name__ == "__main__":
    config_path = "config.yaml"
    server_name = "0.0.0.0"
    server_port = 7860
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                server_name = config.get('ui', {}).get('server_name', server_name)
                server_port = config.get('ui', {}).get('server_port', server_port)
        except Exception as e:
            logger.warning(f"Config load failed: {e}. Using defaults.")
            
    logger.info(f"Deploying Intelligence Dashboard at http://{server_name}:{server_port}")
    demo.launch(server_name=server_name, server_port=server_port, share=False, css=custom_css)
