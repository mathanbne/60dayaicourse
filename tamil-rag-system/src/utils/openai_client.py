"""
OpenAI client for embeddings and LLM interactions
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from openai import OpenAI
from typing import List, Dict, Any
import logging

from config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSIONS,
    LLM_MODEL,
    LLM_TEMPERATURE
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenAIClient:
    """Client for OpenAI API interactions."""
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.embedding_model = EMBEDDING_MODEL
        self.llm_model = LLM_MODEL
        logger.info(f"✅ OpenAI client initialized")
        logger.info(f"   Embedding model: {self.embedding_model}")
        logger.info(f"   LLM model: {self.llm_model}")
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        text = text.replace("\n", " ").strip()
        
        if not text:
            return [0.0] * EMBEDDING_DIMENSIONS
        
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text,
            dimensions=EMBEDDING_DIMENSIONS
        )
        
        return response.data[0].embedding
    
    def get_embeddings_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Generate embeddings for multiple texts in batches."""
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch = [t.replace("\n", " ").strip() for t in batch]
            
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=batch,
                dimensions=EMBEDDING_DIMENSIONS
            )
            
            batch_embeddings = [d.embedding for d in response.data]
            all_embeddings.extend(batch_embeddings)
            
            logger.info(f"  Embedded batch {i//batch_size + 1}: {len(batch)} texts")
        
        return all_embeddings
    
    def generate_response(
        self,
        query: str,
        context: str,
        citations: List[Dict]
    ) -> Dict[str, Any]:
        """Generate a response using retrieved context."""
        
        try:
            system_prompt = """You are a teaching assistant for Samacheer Kalvi textbooks.
RULES:
1. ONLY answer based on the provided context
2. NEVER make up information
3. Cite sources using [Source X] format
4. Answer in Tamil or English based on question language
"""
            
            # Safely build citation text
            citation_lines = []
            if citations:
                for i, c in enumerate(citations):
                    if c is None:
                        continue
                    grade = c.get('grade', 'N/A') if isinstance(c, dict) else 'N/A'
                    term = c.get('term', 'N/A') if isinstance(c, dict) else 'N/A'
                    subject = c.get('subject', 'N/A') if isinstance(c, dict) else 'N/A'
                    page = c.get('page', 'N/A') if isinstance(c, dict) else 'N/A'
                    citation_lines.append(f"[Source {i+1}] Grade {grade}, Term {term}, {subject}, Page {page}")
            
            citation_text = "\n".join(citation_lines) if citation_lines else "No sources available"
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Question: {query}\n\nContext:\n{context}\n\nSources:\n{citation_text}\n\nAnswer based ONLY on the context:"}
            ]
            
            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
                temperature=LLM_TEMPERATURE,
                max_tokens=1000
            )
            
            return {
                "answer": response.choices[0].message.content,
                "model": self.llm_model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        except Exception as e:
            logger.error(f"Generate response error: {e}")
            return {
                "answer": f"Error: {str(e)}",
                "model": self.llm_model,
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            }
        """Generate a response using retrieved context with zero-hallucination."""

    def describe_image(self, image_base64: str, context: str = "") -> str:
        """
        Use GPT-4o Vision to describe an image.
        
        Args:
            image_base64: Base64 encoded image
            context: Optional context about the image (e.g., page number, subject)
        
        Returns:
            Description of the image in Tamil and English
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an educational content analyzer for Tamil textbooks.
Describe images in both Tamil and English. Focus on:
- Educational content (diagrams, charts, illustrations)
- Text visible in the image
- Key concepts being illustrated
- Any Tamil text or labels

Format:
**Tamil:** [Tamil description]
**English:** [English description]
**Key Concepts:** [List main educational concepts]"""
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Describe this image from a Tamil textbook. {context}"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error describing image: {e}")
            return f"[Image description failed: {e}]"


# Singleton instance
_client = None

def get_openai_client() -> OpenAIClient:
    """Get or create OpenAI client singleton."""
    global _client
    if _client is None:
        _client = OpenAIClient()
    return _client


if __name__ == "__main__":
    print("🤖 Testing OpenAI Connection...")
    client = get_openai_client()
    
    # Test Tamil embedding
    tamil_text = "தமிழ் மொழி உலகின் மிகப் பழமையான மொழிகளில் ஒன்று"
    embedding = client.get_embedding(tamil_text)
    print(f"   ✅ Tamil embedding: {len(embedding)} dimensions")
    print(f"   First 5 values: {embedding[:5]}")
    
    print("✅ OpenAI connection test complete!")