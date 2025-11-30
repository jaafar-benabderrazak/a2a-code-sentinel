"""Performance review agent for optimization analysis"""

import json
import re
from agents.llm_client import OllamaClient
from messaging.message import CodeReviewMessage


class PerformanceReviewAgent:
    """Agent specialized in performance optimization"""
    
    def __init__(self, model: str = "qwen2.5-coder:7b"):
        self.agent_id = "performance-agent"
        self.client = OllamaClient(model=model)
        
    async def review(self, message: CodeReviewMessage) -> CodeReviewMessage:
        """Analyze code for performance issues"""
        
        prompt = f"""You are a performance optimization expert. Analyze this {message.language} code for performance issues:

```{message.language}
{message.code_snippet}
```

Look for:
1. N+1 query problems
2. Inefficient algorithms (O(n²) where O(n) possible)
3. Memory leaks
4. Unnecessary network calls
5. Missing caching opportunities
6. Database query optimization
7. Blocking I/O operations

Respond ONLY with valid JSON in this exact format (no additional text):
{{
  "findings": [
    {{
      "type": "performance",
      "severity": "medium",
      "issue": "N+1 query problem in loop",
      "line": "5-7",
      "recommendation": "Use bulk query to fetch all records at once",
      "estimated_impact": "50% faster execution"
    }}
  ],
  "severity_score": 6
}}

If no issues found, return: {{"findings": [], "severity_score": 0}}"""

        response_text = self.client.generate(prompt, max_tokens=2000)
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(response_text)
                
            message.findings.extend(result.get("findings", []))
            message.severity_score = max(message.severity_score, result.get("severity_score", 0))
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Could not parse JSON response from {self.agent_id}")
            print(f"Error: {e}")
            print(f"Raw response: {response_text[:300]}...")
            message.findings.append({
                "type": "performance",
                "severity": "low",
                "issue": "Performance analysis completed but response formatting error occurred",
                "line": "N/A",
                "recommendation": "Manual performance review recommended",
                "estimated_impact": "Unknown"
            })
        
        message.from_agent = self.agent_id
        return message

