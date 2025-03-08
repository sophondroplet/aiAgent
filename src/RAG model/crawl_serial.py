import asyncio
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import requests
from xml.etree import ElementTree
import os

async def crawl_sequential(urls: List[str]):
    print("\n=== Sequential Crawling with Session Reuse ===")

    browser_config = BrowserConfig(
        headless=True,
        # For better performance in Docker or low-memory environments:
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )

    crawl_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator()
    )

    # Create the crawler (opens the browser)
    async with AsyncWebCrawler(config=browser_config) as crawler:
        for i, url in enumerate(urls):
            result = await crawler.arun(
                url=url,
                config=crawl_config
            )
            if result.success:
                print(f"Successfully crawled: {url}")
                # E.g. check markdown length
                print(f"Markdown length: {len(result.markdown_v2.raw_markdown)}")

                output_dir = os.path.join(os.path.dirname(__file__), 'TUAS_wiki')
                os.makedirs(output_dir, exist_ok=True)
                
                file_path = os.path.join(output_dir, f"markdown{i}.txt")
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(result.markdown_v2.raw_markdown)

            else:
                print(f"Failed: {url} - Error: {result.error_message}")

def get_pydantic_ai_docs_urls():
    """
    Fetches all URLs from the Pydantic AI documentation.
    Uses the sitemap (https://ai.pydantic.dev/sitemap.xml) to get these URLs.
    
    Returns:
        List[str]: List of URLs
    """            
    sitemap_url = "https://tritonuas.com/wiki/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        
        # Parse the XML
        root = ElementTree.fromstring(response.content)
        
        # Extract all URLs from the sitemap
        # The namespace is usually defined in the root element
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        
        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

async def main():
    urls = get_pydantic_ai_docs_urls()
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        await crawl_sequential(urls)
    else:
        print("No URLs found to crawl")

if __name__ == "__main__":
    asyncio.run(main())


    


    