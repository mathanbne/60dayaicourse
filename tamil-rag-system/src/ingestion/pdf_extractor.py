"""
PDF Extractor for Tamil Textbooks - Text and Images
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import fitz  # PyMuPDF
import json
import base64
import logging
from typing import List, Dict, Any, Optional
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress MuPDF warnings
fitz.TOOLS.mupdf_display_errors(False)


class PDFExtractor:
    """Extract text and images from Tamil textbook PDFs."""
    
    def __init__(self):
        logger.info("✅ PDF Extractor initialized (Text + Images)")
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract text from PDF page by page."""
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        logger.info(f"📄 Extracting text from: {pdf_path.name}")
        
        pages = []
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            
            if text.strip():
                pages.append({
                    "page_number": page_num + 1,
                    "content": text.strip(),
                    "char_count": len(text)
                })
        
        doc.close()
        
        logger.info(f"   ✅ Extracted {len(pages)} pages with text")
        return pages
    
    def extract_images_from_pdf(
        self, 
        pdf_path: str,
        min_width: int = 100,
        min_height: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Extract images from PDF.
        
        Args:
            pdf_path: Path to PDF file
            min_width: Minimum image width to extract
            min_height: Minimum image height to extract
        
        Returns:
            List of dicts with image data and metadata
        """
        pdf_path = Path(pdf_path)
        logger.info(f"🖼️ Extracting images from: {pdf_path.name}")
        
        images = []
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                
                try:
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    width = base_image["width"]
                    height = base_image["height"]
                    
                    # Skip small images (likely icons or decorations)
                    if width < min_width or height < min_height:
                        continue
                    
                    # Convert to base64
                    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                    
                    images.append({
                        "page_number": page_num + 1,
                        "image_index": img_index,
                        "width": width,
                        "height": height,
                        "format": image_ext,
                        "base64": image_base64,
                        "size_kb": len(image_bytes) / 1024
                    })
                    
                except Exception as e:
                    logger.debug(f"Could not extract image {img_index} from page {page_num + 1}: {e}")
        
        doc.close()
        
        logger.info(f"   ✅ Extracted {len(images)} images")
        return images
    
    def chunk_text(
        self, 
        text: str, 
        chunk_size: int = 500, 
        overlap: int = 50
    ) -> List[str]:
        """Split text into overlapping chunks."""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            if end < len(text):
                for punct in ['।', '.', '!', '?', '\n\n']:
                    last_punct = text[start:end].rfind(punct)
                    if last_punct != -1 and last_punct > chunk_size // 2:
                        end = start + last_punct + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
        
        return chunks
    
    def extract_and_chunk(
        self, 
        pdf_path: str,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> List[Dict[str, Any]]:
        """Extract PDF and create text chunks with metadata."""
        pages = self.extract_text_from_pdf(pdf_path)
        
        all_chunks = []
        chunk_id = 0
        
        for page in pages:
            chunks = self.chunk_text(page["content"], chunk_size, overlap)
            
            for chunk in chunks:
                all_chunks.append({
                    "chunk_id": chunk_id,
                    "page_number": page["page_number"],
                    "content": chunk,
                    "content_type": "text",
                    "char_count": len(chunk)
                })
                chunk_id += 1
        
        logger.info(f"   ✅ Created {len(all_chunks)} text chunks")
        return all_chunks
    
    def process_textbook(
        self,
        pdf_path: str,
        grade: int,
        term: int,
        subject: str = "Tamil",
        extract_images: bool = True
    ) -> Dict[str, Any]:
        """
        Process a complete textbook PDF with text and images.
        """
        # Extract text chunks
        chunks = self.extract_and_chunk(pdf_path)
        
        # Add metadata to each chunk
        for chunk in chunks:
            chunk["grade"] = grade
            chunk["term"] = term
            chunk["subject"] = subject
            chunk["source_file"] = Path(pdf_path).name
        
        # Extract images if requested
        images = []
        if extract_images:
            images = self.extract_images_from_pdf(pdf_path)
            for img in images:
                img["grade"] = grade
                img["term"] = term
                img["subject"] = subject
                img["source_file"] = Path(pdf_path).name
        
        return {
            "grade": grade,
            "term": term,
            "subject": subject,
            "source_file": Path(pdf_path).name,
            "total_text_chunks": len(chunks),
            "total_images": len(images),
            "chunks": chunks,
            "images": images
        }
    
    def save_extracted_data(self, data: Dict, output_path: str):
        """Save extracted data to JSON file (without base64 images)."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create a copy without base64 data (to save space)
        save_data = {**data}
        save_data["images"] = [
            {k: v for k, v in img.items() if k != "base64"} 
            for img in data.get("images", [])
        ]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"   ✅ Saved to: {output_path}")


if __name__ == "__main__":
    from config import TEXTBOOKS_DIR, PROCESSED_DIR
    
    extractor = PDFExtractor()
    
    # Check for Year 6 PDFs
    year_6_dir = TEXTBOOKS_DIR / "year_6"
    
    if year_6_dir.exists():
        pdfs = list(year_6_dir.glob("*.pdf"))
        
        if pdfs:
            print(f"\n📚 Found {len(pdfs)} PDF(s) in {year_6_dir}:")
            for pdf in pdfs:
                print(f"   - {pdf.name}")
            
            # Process first PDF as test
            print(f"\n🔄 Testing extraction on: {pdfs[0].name}")
            data = extractor.process_textbook(
                pdf_path=str(pdfs[0]),
                grade=6,
                term=1,
                subject="Tamil",
                extract_images=True
            )
            
            print(f"\n📊 Results:")
            print(f"   Text chunks: {data['total_text_chunks']}")
            print(f"   Images found: {data['total_images']}")
            
            if data['images']:
                print(f"\n   Sample images:")
                for img in data['images'][:3]:
                    print(f"   - Page {img['page_number']}: {img['width']}x{img['height']} ({img['format']})")
        else:
            print(f"\n⚠️ No PDF files found in: {year_6_dir}")
    else:
        print(f"\n⚠️ Folder not found: {year_6_dir}")