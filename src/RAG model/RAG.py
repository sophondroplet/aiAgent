from __future__ import annotations as _annotations

import asyncio
import os
from dataclasses import dataclass
from typing import Any, Dict

import logfire
from devtools import debug
from httpx import AsyncClient

from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel

from supabase import create_client, Client
import requests 
import json

logfire.configure(send_to_logfire = os.getenv("LOGFIRE_TOKEN"))

@dataclass
class hf_and_db_Deps:
    hf_model_id: str
    hf_url: str
    hf_headers: Dict[str, str]
    db_url: str
    db_key: str
    db_supabase: Client


RAG_agent = Agent(
    model = OpenAIModel(
            'google/gemini-2.0-flash-lite-preview-02-05:free',
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")), 
    
    system_prompt = (
        'You are an expert in Triton UAS, a UCSD club that builds drones.'
        'Use the `retrieve_docs` tool to get relevant documents about Triton UAS.'
        ),
    
    deps_type = hf_and_db_Deps
    )

@RAG_agent.tool
async def retrieve_docs(ctx: RunContext[hf_and_db_Deps], query: str) -> dict[str, Any]:
    """
    Retrieve relevant documents from about Trition UAS.
    """

    #convert query into embedding
    try:
        response = requests.post(url = ctx.deps.hf_url, headers = ctx.deps.hf_headers, json={"inputs": query, "options":{"wait_for_model":True}})
        embedding = response.json()  # Extract JSON content from the response
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return [0] * 384  # Return zero vector on error
    
    response = (
    ctx.deps.db_supabase.rpc(
            'vector_search',
            {
                'query_embedding': embedding,
                'match_count': 3,
                'filter': {'source': 'TUAS_docs'}
            }
        ).execute()
    )
    
    response_data = response.data

    return response_data

async def main():
    hf_model_id = "sentence-transformers/all-MiniLM-L6-v2"
    api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{hf_model_id}"
    headers = {"Authorization": f"Bearer {os.environ['HF_API_KEY']}"}
    
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    deps = hf_and_db_Deps(
        hf_model_id=hf_model_id,
        hf_url=api_url,
        hf_headers=headers,
        db_url=url,
        db_key=key,
        db_supabase = supabase
    )

    user_input = "what is the purpose of the onboarding foam aircraft project?"

    final_response = await RAG_agent.run(user_input, deps=deps)
    print(final_response.data)

if __name__ == "__main__":
    asyncio.run(main())
    
