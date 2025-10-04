#!/usr/bin/env python3
"""
Simple test script to verify the NANDA agent is working correctly.
Run this after setting up your .env file with OPENAI_API_KEY.
"""

import asyncio
import json
import httpx
from app.agent import NandaAgent

async def test_agent():
    """Test the agent with a simple MCP question."""
    try:
        agent = NandaAgent()
        
        # Test message
        messages = [
            {"role": "user", "content": "In 3 bullets, what is MCP (Model Context Protocol)?"}
        ]
        
        print("Testing NANDA Agent...")
        print("Question: In 3 bullets, what is MCP (Model Context Protocol)?")
        print("\nResponse:")
        
        response = await agent.run(messages)
        print(response)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have set OPENAI_API_KEY in your .env file")

async def test_api():
    """Test the FastAPI endpoints."""
    try:
        async with httpx.AsyncClient() as client:
            # Test health endpoint
            print("\nTesting API endpoints...")
            health_response = await client.get("http://127.0.0.1:8080/health")
            print(f"Health check: {health_response.status_code} - {health_response.json()}")
            
            # Test chat endpoint
            chat_data = {
                "messages": [
                    {"role": "user", "content": "What is agent interoperability?"}
                ]
            }
            chat_response = await client.post(
                "http://127.0.0.1:8080/chat",
                json=chat_data,
                headers={"Content-Type": "application/json"}
            )
            print(f"Chat response: {chat_response.status_code}")
            if chat_response.status_code == 200:
                print(f"Reply: {chat_response.json()['reply']}")
            else:
                print(f"Error: {chat_response.text}")
                
    except Exception as e:
        print(f"API test failed: {e}")
        print("Make sure the server is running: uvicorn app.main:app --host 0.0.0.0 --port 8080")

if __name__ == "__main__":
    print("NANDA Agent Test Suite")
    print("=" * 50)
    
    # Test agent directly
    asyncio.run(test_agent())
    
    # Test API (uncomment if server is running)
    # asyncio.run(test_api())
