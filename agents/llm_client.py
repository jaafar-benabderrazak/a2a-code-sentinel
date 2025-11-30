"""LLM client abstraction for open-source models"""

import json
import requests
from typing import Optional, Dict, Any


class OllamaClient:
    """Client for Ollama local LLM"""
    
    def __init__(self, model: str = "qwen2.5-coder:7b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        
    def generate(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.1) -> str:
        """
        Generate completion from Ollama
        
        Args:
            prompt: The prompt to send to the model
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (lower = more deterministic)
            
        Returns:
            Generated text response
        """
        
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result["response"]
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.base_url}. "
                "Make sure Ollama is running: 'ollama serve'"
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(
                f"Request to Ollama timed out. Model {self.model} may be too large or system is overloaded."
            )
    
    def chat(self, messages: list, max_tokens: int = 2000, temperature: float = 0.1) -> str:
        """
        Chat completion using Ollama's chat API
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated response content
        """
        
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result["message"]["content"]
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.base_url}. "
                "Make sure Ollama is running: 'ollama serve'"
            )
    
    def list_models(self) -> list:
        """List available models in Ollama"""
        url = f"{self.base_url}/api/tags"
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("models", [])
    
    def check_model_exists(self) -> bool:
        """Check if the configured model is available"""
        try:
            models = self.list_models()
            return any(m["name"] == self.model for m in models)
        except:
            return False

