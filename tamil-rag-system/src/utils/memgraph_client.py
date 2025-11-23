"""
Memgraph Cloud client with vector search support and auto-reconnect
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, SessionExpired
from typing import List, Dict, Any, Optional
import logging

from config import (
    MEMGRAPH_HOST, 
    MEMGRAPH_PORT,
    MEMGRAPH_USERNAME,
    MEMGRAPH_PASSWORD,
    MEMGRAPH_ENCRYPTED,
    VECTOR_INDEX_CONFIG
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemgraphClient:
    """Client for interacting with Memgraph Cloud with auto-reconnect."""
    
    def __init__(self):
        self.uri = f"bolt+ssc://{MEMGRAPH_HOST}:{MEMGRAPH_PORT}"
        self.auth = (MEMGRAPH_USERNAME, MEMGRAPH_PASSWORD)
        self.driver = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Memgraph Cloud."""
        try:
            if self.driver:
                try:
                    self.driver.close()
                except:
                    pass
            
            self.driver = GraphDatabase.driver(self.uri, auth=self.auth)
            
            # Test connection
            with self.driver.session() as session:
                result = session.run("RETURN 'Connected!' AS message")
                msg = result.single()["message"]
                
            logger.info(f"✅ Connected to Memgraph Cloud at {MEMGRAPH_HOST}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Memgraph: {e}")
            raise
    
    def _reconnect_if_needed(self):
        """Check connection and reconnect if needed."""
        try:
            with self.driver.session() as session:
                session.run("RETURN 1")
        except (ServiceUnavailable, SessionExpired, OSError) as e:
            logger.warning("🔄 Connection lost, reconnecting...")
            self._connect()
    
    def close(self):
        """Close the database connection."""
        if self.driver:
            self.driver.close()
            logger.info("Memgraph connection closed")
    
    def execute_query(self, query: str, parameters: Dict = None) -> List[Dict]:
        """Execute a Cypher query and return results with auto-reconnect."""
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except (ServiceUnavailable, SessionExpired, OSError) as e:
            logger.warning("🔄 Connection lost, reconnecting...")
            self._connect()
            # Retry once
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
    
    def execute_write(self, query: str, parameters: Dict = None) -> None:
        """Execute a write query with auto-reconnect."""
        try:
            with self.driver.session() as session:
                session.run(query, parameters or {})
        except (ServiceUnavailable, SessionExpired, OSError) as e:
            logger.warning("🔄 Connection lost, reconnecting...")
            self._connect()
            # Retry once
            with self.driver.session() as session:
                session.run(query, parameters or {})
    
    def setup_vector_indexes(self):
        """Create vector indexes for semantic search."""
        logger.info("Setting up vector indexes...")
        
        dimension = VECTOR_INDEX_CONFIG["dimension"]
        capacity = VECTOR_INDEX_CONFIG["capacity"]
        
        indexes = [
            ("paragraph_vector_idx", "Paragraph", "embedding"),
            ("question_vector_idx", "Question", "embedding"),
            ("vocabulary_vector_idx", "Vocabulary", "embedding"),
        ]
        
        for idx_name, label, prop in indexes:
            query = f"""
            CREATE VECTOR INDEX {idx_name}
            ON :{label}({prop})
            WITH CONFIG {{"dimension": {dimension}, "capacity": {capacity}, "metric": "cos"}}
            """
            try:
                self.execute_write(query)
                logger.info(f"  ✅ Created: {idx_name}")
            except Exception as e:
                if "already exists" in str(e).lower():
                    logger.info(f"  ⏭️ Already exists: {idx_name}")
                else:
                    logger.warning(f"  ⚠️ {idx_name}: {e}")
        
        logger.info("✅ Vector indexes setup complete")
    
    def clear_database(self):
        """Clear all data from database. USE WITH CAUTION!"""
        logger.warning("⚠️ Clearing all data from Memgraph...")
        self.execute_write("MATCH (n) DETACH DELETE n")
        logger.info("✅ Database cleared")
    
    def get_stats(self) -> Dict:
        """Get database statistics."""
        node_count = self.execute_query("MATCH (n) RETURN count(n) as count")[0]["count"]
        rel_count = self.execute_query("MATCH ()-[r]->() RETURN count(r) as count")[0]["count"]
        return {"nodes": node_count, "relationships": rel_count}


# Singleton instance
_client = None

def get_memgraph_client() -> MemgraphClient:
    """Get or create Memgraph client singleton."""
    global _client
    if _client is None:
        _client = MemgraphClient()
    return _client


if __name__ == "__main__":
    print("🔷 Testing Memgraph Cloud Connection...")
    client = get_memgraph_client()
    
    stats = client.get_stats()
    print(f"   Nodes: {stats['nodes']}, Relationships: {stats['relationships']}")
    
    client.close()
    print("✅ Memgraph Cloud connection test complete!")