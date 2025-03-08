import supabase
import os
import asyncio
from supabase import create_client, Client
from RAG_embeddings import ProcessedChunk

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


async def insert_chunk(chunk: ProcessedChunk):
    response = (
        supabase.table("PydanticAI_docs")
        .insert(chunk.__dict__)
        .execute()
    )
    
    print(f"Inserted chunk {chunk.chunk_number} for {chunk.url}")

