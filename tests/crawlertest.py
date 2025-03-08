import asyncio
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import requests
from xml.etree import ElementTree
import os

from RAG_textchunk import chunk_text
from tests.test_RAG_embeddings import process_chunk
from RAG_supabase import insert_chunk


async def process_and_store_doc(url: str, doc: str):
    chunks = chunk_text(doc)
    process_tasks = [process_chunk(chunk, i, url) 
                     for i, chunk in enumerate(chunks)]
    processed_chunks = await asyncio.gather(*process_tasks)
    
    insert_tasks = [insert_chunk(processed_chunk)
                   for processed_chunk in processed_chunks]
    await asyncio.gather(*insert_tasks)

async def crawl_website(urls: List[str]):
    print("\n=== Sequential Crawling with Session Reuse ===")

    browser_config = BrowserConfig(
        headless=True,
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
            # print(f"Successfully crawled: {url}")
            # # E.g. check markdown length
            # print(f"Markdown length: {len(result.markdown_v2.raw_markdown)}")

            # #write the result to a file
            
            # output_dir = os.path.join(os.path.dirname(__file__), 'WeatherAgent_docs')
            # os.makedirs(output_dir, exist_ok=True)
                
            # file_path = os.path.join(output_dir, f"markdown_raw.txt")

            # with open(file_path, "w", encoding="utf-8") as f:
            #     f.write(result.markdown_v2.raw_markdown)

                await process_and_store_doc(url, result.markdown_v2.raw_markdown)

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
    await crawl_website(urls)

    # for i, chunk in enumerate(chunks):
    #     processed_chunk = await process_chunk(chunk, i)
    #     print(processed_chunk)

if __name__ == "__main__":
    asyncio.run(main())



