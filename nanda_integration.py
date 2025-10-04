#!/usr/bin/env python3
"""
NANDA Integration Script for the Trust-First Agentic Web Explainer
This script wraps our LangChain agent with the NANDA adapter for global agent interoperability.
"""

import os
import asyncio
from nanda_adapter import NANDA
from app.agent import NandaAgent

def create_nanda_improvement():
    """Create the improvement function that NANDA expects."""
    
    # Initialize our agent
    agent = NandaAgent()
    
    def nanda_improvement(message_text: str) -> str:
        """Transform messages using our Trust-First Agentic Web Explainer."""
        try:
            # Create messages in the format our agent expects
            messages = [
                {"role": "user", "content": message_text}
            ]
            
            # Run the agent (we need to handle async in sync context)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(agent.run(messages))
                return response
            finally:
                loop.close()
                
        except Exception as e:
            print(f"Error in NANDA improvement: {e}")
            return f"Error processing message: {e}"
    
    return nanda_improvement

def main():
    """Main function to start the NANDA-wrapped agent."""
    print("Starting Trust-First Agentic Web Explainer with NANDA adapter...")
    
    # Create our improvement function
    improvement_function = create_nanda_improvement()
    
    # Initialize NANDA with our function
    nanda = NANDA(improvement_function)
    
    # Get environment variables
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    domain = os.getenv("DOMAIN_NAME")
    
    if not anthropic_key:
        print("Error: ANTHROPIC_API_KEY environment variable is required")
        print("Please set it with: export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    if not domain:
        print("Warning: DOMAIN_NAME not set, using localhost for testing")
        domain = "localhost"
    
    print(f"Starting NANDA server on domain: {domain}")
    print("The agent will be available for global agent-to-agent communication!")
    
    # Start the NANDA server
    nanda.start_server_api(anthropic_key, domain)

if __name__ == "__main__":
    main()
