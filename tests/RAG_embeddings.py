import asyncio
import requests
import os
from dataclasses import dataclass
from typing import List, Dict, Any
from openai import AsyncOpenAI
import json

#openrounter client setup

openrouter_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

#hugging face embedding model setup

hf_token = os.environ["HF_API_KEY"]
model_id = "sentence-transformers/all-MiniLM-L6-v2"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

#get a title and summary for the chunk

async def get_title_and_summary(chunk: str, url: str = "Not available") -> Dict[str, str]:
    system_prompt = """You are an AI that extracts titles and summaries from documentation chunks.
    Return a JSON object with 'title' and 'summary' keys.
    For the title: If this seems like the start of a document, extract its title. If it's a middle chunk, derive a descriptive title.
    For the summary: Create a concise summary of the main points in this chunk.
    Keep both title and summary concise but informative."""
    
    try:
        response = await openrouter_client.chat.completions.create(
            model="google/gemini-2.0-flash-lite-preview-02-05:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"URL: {url}\n\nContent:\n{chunk[:1000]}..."}  # Send first 1000 chars for context
            ],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        print(f"Error getting title and summary: {e}")
        return {"title": "Error processing title", "summary": "Error processing summary"}

#get the embedding for the chunk

async def get_embedding(chunk: str) -> List[float]:
    response = requests.post(api_url, headers=headers, json={"inputs": chunk, "options":{"wait_for_model":True}})
    return response.json()

#datamodel for processed chunk

@dataclass
class ProcessedChunk:
    url: str
    chunk_number: int
    title: str
    summary: str
    content: str
    metadata: Dict[str, Any]
    embedding: List[float]

#process a single chunk of text

async def process_chunk(chunk: str, chunk_number: int, url: str = "NA") -> ProcessedChunk:
    """Process a single chunk of text."""
    # Get title and summary
    extracted = await get_title_and_summary(chunk, url)
    
    # Get embedding
    embedding = await get_embedding(chunk)
    
    # Create metadata
    metadata = {
        "source": "pydantic_ai_docs",
        "chunk_size": len(chunk),
        "crawled_at": "NA",
        "url_path": url
    }
    

    try:
        title_extracted = extracted['title']
        summary_extracted = extracted['summary']
    
    except:
        print ("tyep error with summary")
        print (extracted )

    return ProcessedChunk(
        url=url,
        chunk_number=chunk_number,
        title=title_extracted,
        summary=summary_extracted,
        content=chunk,  # Store the original chunk content
        metadata=metadata,
        embedding=embedding
    )


    