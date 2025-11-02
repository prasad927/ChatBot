from backend.services.logger import logger
from langchain_community.vectorstores import FAISS
from typing import Optional


class DocumentSearchTool:

    """Custom tool for searching uploaded documents."""
    
    def __init__(self, vectorstore: Optional[FAISS] = None):
        self.vectorstore = vectorstore


    def search(self, query: str) -> str:
        """Search the uploaded document for relevant information."""

        if not self.vectorstore:
            return "No document has been uploaded yet. Please upload a PDF first."
        
        try:
            # Search for relevant documents
            docs = self.vectorstore.similarity_search(query, k=4)
            
            if not docs:
                return "No relevant information found in the document."
            
            # Format results
            results = []
            for i, doc in enumerate(docs, 1):
                page = doc.metadata.get('page', 'N/A')
                content = doc.page_content[:300]  # First 300 chars
                results.append(f"[Source {i} - Page {page}]\n{content}...")
            
            return "\n\n".join(results)
        
        except Exception as e:
            logger.error(f"Error in document search: {e}")
            return f"Error searching document: {str(e)}"
    

    def update_vectorstore(self, vectorstore: FAISS):
        """Update the vectorstore when a new document is uploaded."""
        self.vectorstore = vectorstore
    