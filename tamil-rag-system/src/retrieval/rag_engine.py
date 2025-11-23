"""
RAG Engine - Hybrid Vector + Graph Search for Zero Hallucination
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import logging
from typing import List, Dict, Any, Optional

from src.utils.memgraph_client import get_memgraph_client
from src.utils.openai_client import get_openai_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGEngine:
    """RAG Engine with Zero Hallucination."""
    
    def __init__(self):
        self.mg = get_memgraph_client()
        self.openai = get_openai_client()
        logger.info("✅ RAG Engine initialized")
    
    def vector_search(
        self, 
        query: str, 
        top_k: int = 5,
        grade: Optional[int] = None,
        include_images: bool = True
    ) -> List[Dict]:
        """Perform vector similarity search on both text and images."""
        
        try:
            # Generate query embedding
            query_embedding = self.openai.get_embedding(query)
            embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"
            
            all_results = []
            
            # Search paragraphs
            text_top_k = top_k if not include_images else max(3, top_k // 2)
            cypher_text = f"""
            CALL vector_search.search('paragraph_vector_idx', {text_top_k}, {embedding_str})
            YIELD node, score
            OPTIONAL MATCH (t:Term)-[:CONTAINS]->(node)
            RETURN 
                node.id AS chunk_id,
                node.content AS content,
                node.page_number AS page,
                score AS relevance_score,
                t.grade AS grade,
                t.number AS term,
                t.subject AS subject,
                'text' AS content_type
            """
            
            text_results = self.mg.execute_query(cypher_text, {})
            
            # Search images if enabled
            if include_images:
                image_top_k = max(2, top_k // 2)
                try:
                    cypher_image = f"""
                    CALL vector_search.search('image_vector_idx', {image_top_k}, {embedding_str})
                    YIELD node, score
                    OPTIONAL MATCH (t:Term)-[:CONTAINS]->(node)
                    RETURN 
                        node.id AS chunk_id,
                        node.description AS content,
                        node.page_number AS page,
                        score AS relevance_score,
                        t.grade AS grade,
                        t.number AS term,
                        t.subject AS subject,
                        'image' AS content_type
                    """
                    image_results = self.mg.execute_query(cypher_image, {})
                    # Filter out None results before combining
                    image_results = [r for r in image_results if r is not None]
                    all_results = text_results + image_results
                except Exception as e:
                    logger.warning(f"Image search failed: {e}, using text only")
                    all_results = text_results
            else:
                all_results = text_results
            
            # Filter out None values before sorting
            all_results = [r for r in all_results if r is not None]
            
            if not all_results:
                return []
            
            # Sort by relevance score and take top_k (handle None values)
            all_results = sorted(
                all_results, 
                key=lambda x: x.get('relevance_score') if x.get('relevance_score') is not None else 0.0, 
                reverse=True
            )[:top_k]
            
            # Clean and validate results
            clean_results = []
            for r in all_results:
                if r is None:
                    continue
                content = r.get('content') if r else None
                if not content:
                    continue
                    
                clean_results.append({
                    'chunk_id': r.get('chunk_id') or 'unknown',
                    'content': content,
                    'page': r.get('page') or 0,
                    'relevance_score': r.get('relevance_score') or 0.0,
                    'grade': r.get('grade') or 6,
                    'term': r.get('term') or 1,
                    'subject': r.get('subject') or 'General',
                    'content_type': r.get('content_type', 'text')
                })
            
            return clean_results
            
        except Exception as e:
            logger.error(f"Vector search error: {e}")
            return []
    
    def build_context(self, search_results: List[Dict]) -> str:
        """Build context string from search results."""
        if not search_results:
            return ""
            
        context_parts = []
        for i, result in enumerate(search_results, 1):
            if result is None:
                continue
            content_type = result.get('content_type', 'text')
            type_label = "[IMAGE]" if content_type == 'image' else "[TEXT]"
            
            context_parts.append(
                f"[Source {i}] {type_label} (Grade {result.get('grade', 'N/A')}, "
                f"Term {result.get('term', 'N/A')}, "
                f"{result.get('subject', 'N/A')}, "
                f"Page {result.get('page', 'N/A')}):\n"
                f"{result.get('content', '')}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def build_citations(self, search_results: List[Dict]) -> List[Dict]:
        """Build citation list from search results."""
        if not search_results:
            return []
            
        citations = []
        for i, r in enumerate(search_results):
            if r is None:
                continue
            citations.append({
                "source_id": i + 1,
                "chunk_id": r.get("chunk_id") or "unknown",
                "grade": r.get("grade") or 6,
                "term": r.get("term") or 1,
                "page": r.get("page") or 0,
                "subject": r.get("subject") or "General",
                "relevance_score": r.get("relevance_score") or 0.0,
                "content_type": r.get("content_type", "text")
            })
        
        return citations
    
    def query(
        self,
        question: str,
        top_k: int = 5,
        grade: Optional[int] = None
    ) -> Dict[str, Any]:
        """Complete RAG pipeline."""
        
        logger.info(f"🔍 Query: {question[:50]}...")
        
        # Default response
        default_response = {
            "answer": "மன்னிக்கவும், இந்த கேள்விக்கான தகவல் கிடைக்கவில்லை.",
            "sources": [],
            "confidence": 0.0,
            "usage": {"total_tokens": 0}
        }
        
        try:
            # Step 1: Vector search
            search_results = self.vector_search(question, top_k, grade)
            
            if not search_results or len(search_results) == 0:
                logger.warning("No search results found")
                return default_response
            
            # Step 2: Build context and citations
            context = self.build_context(search_results)
            citations = self.build_citations(search_results)
            
            if not context:
                logger.warning("Empty context")
                return default_response
            
            # Step 3: Generate answer
            response = self.openai.generate_response(
                query=question,
                context=context,
                citations=citations
            )
            
            if response is None:
                logger.error("Response is None")
                return default_response
            
            # Calculate confidence
            scores = [r.get("relevance_score") or 0.0 for r in search_results if r]
            avg_score = sum(scores) / len(scores) if scores else 0.0
            
            return {
                "answer": response.get("answer") or "No answer generated",
                "sources": citations,
                "confidence": round(avg_score, 4),
                "usage": response.get("usage") or {"total_tokens": 0}
            }
            
        except Exception as e:
            logger.error(f"Query error: {e}")
            return {
                "answer": f"Error: {str(e)}",
                "sources": [],
                "confidence": 0.0,
                "usage": {"total_tokens": 0}
            }


def main():
    """Interactive testing."""
    print("\n" + "="*60)
    print("🎓 Tamil Textbook RAG System")
    print("="*60)
    
    engine = RAGEngine()
    
    while True:
        question = input("\n📝 Question (or 'quit'): ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        if not question:
            continue
        
        result = engine.query(question, top_k=3)
        
        print(f"\n📖 Answer:\n{result['answer']}")
        print(f"\n📚 Sources: {len(result['sources'])}")
        for src in result['sources']:
            print(f"   - Grade {src['grade']}, {src['subject']}, Page {src['page']}")


if __name__ == "__main__":
    main()