"""
Load extracted content into Memgraph with embeddings and image descriptions
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import json
import logging
from typing import List, Dict, Any
from tqdm import tqdm

from src.utils.memgraph_client import get_memgraph_client
from src.utils.openai_client import get_openai_client
from src.ingestion.pdf_extractor import PDFExtractor
from config import TEXTBOOKS_DIR, PROCESSED_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphLoader:
    """Load textbook content into Memgraph with vector embeddings and image descriptions."""
    
    def __init__(self):
        self.mg = get_memgraph_client()
        self.openai = get_openai_client()
        self.extractor = PDFExtractor()
        logger.info("✅ GraphLoader initialized (Text + Images)")
    
    def setup_schema(self):
        """Create the knowledge graph schema."""
        logger.info("📊 Setting up graph schema...")
        
        queries = [
            "MERGE (g:Grade {number: $grade}) SET g.name = $name",
            "MERGE (s:Subject {name: $subject})",
            """
            MATCH (g:Grade {number: $grade})
            MATCH (s:Subject {name: $subject})
            MERGE (g)-[:HAS_SUBJECT]->(s)
            """,
        ]
        
        # Setup for Grade 6
        subjects = ["Tamil", "English", "Mathematics", "Science", "Social Science"]
        
        self.mg.execute_write(queries[0], {"grade": 6, "name": "Year 6"})
        
        for subject in subjects:
            self.mg.execute_write(queries[1], {"subject": subject})
            self.mg.execute_write(queries[2], {"grade": 6, "subject": subject})
        
        logger.info("   ✅ Schema created")
    
    def create_vector_indexes(self):
        """Create vector indexes for semantic search."""
        logger.info("🔍 Creating vector indexes...")
        self.mg.setup_vector_indexes()
        
        # Add image index
        try:
            self.mg.execute_write("""
                CREATE VECTOR INDEX image_vector_idx
                ON :Image(embedding)
                WITH CONFIG {"dimension": 1536, "capacity": 50000, "metric": "cos"}
            """)
            logger.info("  ✅ Created: image_vector_idx")
        except Exception as e:
            if "already exists" in str(e).lower():
                logger.info("  ⏭️ Already exists: image_vector_idx")
    
    def detect_subject(self, filename: str) -> str:
        """Detect subject from filename."""
        filename_lower = filename.lower()
        if "tamil" in filename_lower:
            return "Tamil"
        elif "english" in filename_lower:
            return "English"
        elif "math" in filename_lower:
            return "Mathematics"
        elif "science" in filename_lower and "social" not in filename_lower:
            return "Science"
        elif "social" in filename_lower:
            return "Social Science"
        else:
            return "General"
    
    def load_chunks_with_embeddings(
        self, 
        chunks: List[Dict], 
        grade: int,
        term: int,
        subject: str,
        batch_size: int = 50
    ):
        """Load text chunks into Memgraph with embeddings."""
        logger.info(f"📥 Loading {len(chunks)} text chunks...")
        
        # Create Term node
        self.mg.execute_write("""
            MATCH (s:Subject {name: $subject})
            MERGE (t:Term {number: $term, grade: $grade, subject: $subject})
            MERGE (s)-[:HAS_TERM]->(t)
        """, {"term": term, "grade": grade, "subject": subject})
        
        # Process in batches
        for i in tqdm(range(0, len(chunks), batch_size), desc="Loading text"):
            batch = chunks[i:i + batch_size]
            
            texts = [c["content"] for c in batch]
            embeddings = self.openai.get_embeddings_batch(texts)
            
            for chunk, embedding in zip(batch, embeddings):
                chunk_id = f"G{grade}_T{term}_{subject[:3]}_C{chunk['chunk_id']}"
                
                self.mg.execute_write("""
                    MATCH (t:Term {number: $term, grade: $grade, subject: $subject})
                    CREATE (p:Paragraph {
                        id: $chunk_id,
                        content: $content,
                        page_number: $page,
                        chunk_index: $chunk_index,
                        content_type: 'text',
                        embedding: $embedding
                    })
                    CREATE (t)-[:CONTAINS]->(p)
                """, {
                    "term": term,
                    "grade": grade,
                    "subject": subject,
                    "chunk_id": chunk_id,
                    "content": chunk["content"],
                    "page": chunk["page_number"],
                    "chunk_index": chunk["chunk_id"],
                    "embedding": embedding
                })
        
        logger.info(f"   ✅ Loaded {len(chunks)} text chunks")
    
    def load_images_with_descriptions(
        self,
        images: List[Dict],
        grade: int,
        term: int,
        subject: str,
        max_images: int = 50  # Limit to control API costs
    ):
        """Load images with GPT-4o Vision descriptions."""
        
        if not images:
            logger.info("   ⏭️ No images to process")
            return
        
        # Limit images to control costs
        images_to_process = images[:max_images]
        
        logger.info(f"🖼️ Processing {len(images_to_process)} images (of {len(images)} total)...")
        logger.info(f"   ⚠️ Using GPT-4o Vision - this may take a while and cost more")
        
        for i, img in enumerate(tqdm(images_to_process, desc="Processing images")):
            try:
                # Get description from GPT-4o Vision
                context = f"Page {img['page_number']}, {subject} textbook, Grade {grade}"
                description = self.openai.describe_image(img["base64"], context)
                
                # Generate embedding for the description
                embedding = self.openai.get_embedding(description)
                
                # Store in graph
                image_id = f"G{grade}_T{term}_{subject[:3]}_IMG{i}"
                
                self.mg.execute_write("""
                    MATCH (t:Term {number: $term, grade: $grade, subject: $subject})
                    CREATE (img:Image {
                        id: $image_id,
                        page_number: $page,
                        width: $width,
                        height: $height,
                        format: $format,
                        description: $description,
                        content_type: 'image',
                        embedding: $embedding
                    })
                    CREATE (t)-[:CONTAINS]->(img)
                """, {
                    "term": term,
                    "grade": grade,
                    "subject": subject,
                    "image_id": image_id,
                    "page": img["page_number"],
                    "width": img["width"],
                    "height": img["height"],
                    "format": img["format"],
                    "description": description,
                    "embedding": embedding
                })
                
            except Exception as e:
                logger.warning(f"   ⚠️ Failed to process image {i}: {e}")
        
        logger.info(f"   ✅ Loaded {len(images_to_process)} images with descriptions")
    
    def process_and_load_pdf(
        self,
        pdf_path: str,
        grade: int,
        term: int,
        include_images: bool = True,
        max_images: int = 50
    ):
        """Complete pipeline: Extract → Embed → Load to Graph"""
        
        # Detect subject from filename
        subject = self.detect_subject(Path(pdf_path).name)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"📚 Processing: {Path(pdf_path).name}")
        logger.info(f"   Grade: {grade}, Term: {term}, Subject: {subject}")
        logger.info(f"{'='*60}")
        
        # Extract content
        data = self.extractor.process_textbook(
            pdf_path, grade, term, subject, 
            extract_images=include_images
        )
        
        # Save extracted data
        output_file = PROCESSED_DIR / f"grade_{grade}_term_{term}_{subject}.json"
        self.extractor.save_extracted_data(data, str(output_file))
        
        # Load text chunks
        self.load_chunks_with_embeddings(data["chunks"], grade, term, subject)
        
        # Load images (optional)
        if include_images and data["images"]:
            self.load_images_with_descriptions(
                data["images"], grade, term, subject, max_images
            )
        
        logger.info(f"\n✅ Complete! Text: {len(data['chunks'])}, Images: {len(data.get('images', []))}")
        
        return data
    
    def get_stats(self) -> Dict:
        """Get current graph statistics."""
        stats = self.mg.get_stats()
        
        paragraphs = self.mg.execute_query(
            "MATCH (p:Paragraph) RETURN count(p) as count"
        )[0]["count"]
        
        images = self.mg.execute_query(
            "MATCH (i:Image) RETURN count(i) as count"
        )[0]["count"]
        
        return {
            **stats,
            "paragraphs": paragraphs,
            "images": images
        }


def main():
    """Main function to load textbooks."""
    loader = GraphLoader()
    
    # Setup
    loader.setup_schema()
    loader.create_vector_indexes()
    
    # Find all PDFs in all year directories
    all_pdfs = []
    for year_dir in sorted(TEXTBOOKS_DIR.glob("year_*")):
        if year_dir.is_dir():
            pdfs = list(year_dir.glob("*.pdf"))
            for pdf in pdfs:
                # Extract grade from directory name (year_6 -> 6, year_7 -> 7, etc.)
                grade = int(year_dir.name.split("_")[1])
                all_pdfs.append((pdf, grade))
    
    if not all_pdfs:
        print(f"⚠️ No PDFs found in {TEXTBOOKS_DIR}")
        return
    
    print(f"\n📚 Found {len(all_pdfs)} PDF(s) across all grades:")
    for i, (pdf, grade) in enumerate(all_pdfs, 1):
        print(f"   {i}. Grade {grade}: {pdf.name}")
    
    # Ask about images
    print(f"\n⚠️ Image processing uses GPT-4o Vision (costs ~$0.01-0.03 per image)")
    include_images = input("Include images? (y/n): ").strip().lower() == 'y'
    
    max_images = 20
    if include_images:
        max_images = int(input("Max images per PDF (default 20): ").strip() or "20")
    
    # Confirm
    confirm = input("\nProceed with loading? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return
    
    # Process each PDF with detected grade
    for i, (pdf, grade) in enumerate(all_pdfs, 1):
        # Try to detect term from filename
        term = 1  # default
        filename_lower = pdf.name.lower()
        if "term_2" in filename_lower or "term-2" in filename_lower:
            term = 2
        elif "term_3" in filename_lower or "term-3" in filename_lower:
            term = 3
        
        loader.process_and_load_pdf(
            pdf_path=str(pdf),
            grade=grade,
            term=term,
            include_images=include_images,
            max_images=max_images
        )
    
    # Final stats
    stats = loader.get_stats()
    print(f"\n{'='*60}")
    print(f"📊 Final Graph Statistics:")
    print(f"   Total Nodes: {stats['nodes']}")
    print(f"   Total Relationships: {stats['relationships']}")
    print(f"   Text Paragraphs: {stats['paragraphs']}")
    print(f"   Images: {stats['images']}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()