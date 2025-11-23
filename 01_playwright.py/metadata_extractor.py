from playwright.sync_api import sync_playwright
from datetime import datetime

print("=" * 60)
print("METADATA EXTRACTOR - THE HINDU")
print("=" * 60)

try:
    with sync_playwright() as p:
        print("\n[1/4] Launching browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print("[2/4] Opening wikisource.org/wiki/Main_Page...")
        page.goto('https://en.wikisource.org/wiki/Main_Page', wait_until='domcontentloaded')
        page.wait_for_load_state('networkidle')
        
        print("[3/4] Extracting metadata...")
        
        # Collect all metadata
        metadata = []
        metadata.append("=" * 60)
        metadata.append("METADATA EXTRACTION REPORT")
        metadata.append("=" * 60)
        metadata.append(f"\nWebsite: https://www.thehindu.com")
        metadata.append(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        metadata.append("\n" + "=" * 60)
        
        # Page Title
        metadata.append("\n[PAGE TITLE]")
        metadata.append(page.title())
        
        # Page URL
        metadata.append("\n[CURRENT URL]")
        metadata.append(page.url)
        
        # Get all meta tags
        meta_tags = page.locator('meta').all()
        
        # Standard Meta Tags
        metadata.append("\n" + "=" * 60)
        metadata.append("[STANDARD META TAGS]")
        metadata.append("=" * 60)
        
        for meta in meta_tags:
            name = meta.get_attribute('name')
            property_attr = meta.get_attribute('property')
            content = meta.get_attribute('content')
            
            if name and content:
                metadata.append(f"\n{name}:")
                metadata.append(f"  {content}")
            elif property_attr and content:
                metadata.append(f"\n{property_attr}:")
                metadata.append(f"  {content}")
        
        # Open Graph Tags
        metadata.append("\n" + "=" * 60)
        metadata.append("[OPEN GRAPH (OG) TAGS]")
        metadata.append("=" * 60)
        
        og_tags = page.locator('meta[property^="og:"]').all()
        for og in og_tags:
            property_attr = og.get_attribute('property')
            content = og.get_attribute('content')
            if property_attr and content:
                metadata.append(f"\n{property_attr}:")
                metadata.append(f"  {content}")
        
        # Twitter Card Tags
        metadata.append("\n" + "=" * 60)
        metadata.append("[TWITTER CARD TAGS]")
        metadata.append("=" * 60)
        
        twitter_tags = page.locator('meta[name^="twitter:"]').all()
        for twitter in twitter_tags:
            name = twitter.get_attribute('name')
            content = twitter.get_attribute('content')
            if name and content:
                metadata.append(f"\n{name}:")
                metadata.append(f"  {content}")
        
        # Charset
        metadata.append("\n" + "=" * 60)
        metadata.append("[CHARACTER ENCODING]")
        metadata.append("=" * 60)
        
        charset = page.locator('meta[charset]').first
        if charset:
            charset_value = charset.get_attribute('charset')
            metadata.append(f"\nCharset: {charset_value}")
        
        # Viewport
        viewport = page.locator('meta[name="viewport"]').first
        if viewport:
            viewport_content = viewport.get_attribute('content')
            metadata.append(f"Viewport: {viewport_content}")
        
        # Link Tags (canonical, alternate, etc.)
        metadata.append("\n" + "=" * 60)
        metadata.append("[LINK TAGS]")
        metadata.append("=" * 60)
        
        # Canonical URL
        canonical = page.locator('link[rel="canonical"]').first
        if canonical:
            canonical_href = canonical.get_attribute('href')
            metadata.append(f"\nCanonical URL:")
            metadata.append(f"  {canonical_href}")
        
        # Alternate links
        alternate_links = page.locator('link[rel="alternate"]').all()
        if alternate_links:
            metadata.append(f"\nAlternate Links:")
            for link in alternate_links:
                href = link.get_attribute('href')
                hreflang = link.get_attribute('hreflang')
                link_type = link.get_attribute('type')
                if hreflang:
                    metadata.append(f"  Language ({hreflang}): {href}")
                elif link_type:
                    metadata.append(f"  Type ({link_type}): {href}")
                else:
                    metadata.append(f"  {href}")
        
        # Additional Page Info
        metadata.append("\n" + "=" * 60)
        metadata.append("[ADDITIONAL PAGE INFO]")
        metadata.append("=" * 60)
        
        # Get all headings
        h1_tags = page.locator('h1').all()
        if h1_tags:
            metadata.append(f"\nH1 Headings ({len(h1_tags)}):")
            for i, h1 in enumerate(h1_tags[:5], 1):  # Limit to first 5
                text = h1.inner_text()
                if text.strip():
                    metadata.append(f"  {i}. {text.strip()}")
        
        # Get language
        html_lang = page.locator('html').first.get_attribute('lang')
        if html_lang:
            metadata.append(f"\nHTML Language: {html_lang}")
        
        print("[4/4] Saving to file...")
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wikipedia_metadata_{timestamp}.txt"
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(metadata))
        
        print(f"\n✓ Metadata extracted successfully!")
        print(f"✓ Saved to: {filename}")
        
        # Close browser
        browser.close()
        
except Exception as e:
    print(f"\n❌ Error occurred: {e}")
    print("\nMake sure Playwright is installed:")
    print("  pip install playwright")
    print("  playwright install chromium")

print("\n" + "=" * 60)
print("SCRIPT COMPLETE")
print("=" * 60)