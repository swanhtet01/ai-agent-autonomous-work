#!/usr/bin/env python3
"""
Claude Integration for AgentForce - Direct API Access
Each agent can now communicate directly with Claude for assistance
"""

import anthropic
import asyncio
import json
import os
from datetime import datetime

class AgentClaudeIntegration:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
    async def ask_claude(self, question, context=""):
        """Agent asks Claude for help"""
        prompt = f"""
Agent: {self.agent_name}
Question: {question}
Context: {context}

Please provide specific, actionable guidance for this agent.
"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                "success": True,
                "response": response.content[0].text,
                "agent": self.agent_name,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False, 
                "error": str(e),
                "agent": self.agent_name
            }
    
    def claude_code_review(self, code_snippet):
        """Claude reviews agent's code"""
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=1500,
                messages=[{
                    "role": "user", 
                    "content": f"Review this code for bugs and improvements:\n\n{code_snippet}"
                }]
            )
            
            return {
                "success": True,
                "review": response.content[0].text,
                "agent": self.agent_name
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def claude_problem_solve(self, problem):
        """Claude helps solve agent problems"""
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-latest", 
                max_tokens=1500,
                messages=[{
                    "role": "user",
                    "content": f"Agent {self.agent_name} needs help with: {problem}\n\nProvide step-by-step solution."
                }]
            )
            
            return {
                "success": True,
                "solution": response.content[0].text,
                "agent": self.agent_name
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

# Example usage for agents
if __name__ == "__main__":
    # Each agent creates its own Claude integration
    try:
        agent = AgentClaudeIntegration("Test_Agent")
        
        # Test Claude connection
        test_response = agent.client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=100,
            messages=[{"role": "user", "content": "Test connection from AgentForce"}]
        )
        
        print("✅ Claude Integration Test: SUCCESS")
        print(f"Response: {test_response.content[0].text[:100]}...")
        
    except Exception as e:
        print(f"❌ Claude Integration Test: FAILED - {e}")