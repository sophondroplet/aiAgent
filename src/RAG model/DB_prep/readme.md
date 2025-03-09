# DB Preparation

This directory is dedicated to scraping documentation and storing it into Supabase.

## How to Run

Run `RAG_crawl` (the entry point of the program).

## Workflow

1. Crawl the website to get documentation (in Markdown format).
2. Chunk down the Markdown text.
3. Convert chunks into embeddings.
4. Insert each chunk into Supabase.

