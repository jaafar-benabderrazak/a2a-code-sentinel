"""Best practices agent for code quality review"""

import json
import re
from agents.llm_client import OllamaClient
from messaging.message import CodeReviewMessage


class BestPracticesAgent:
    """Agent for code quality and best practices"""
    
    def __init__(self, model: str = "qwen2.5-coder:7b"):
        self.agent_id = "best-practices-agent"
        self.client = OllamaClient(model=model)
        
    async def review(self, message: CodeReviewMessage) -> CodeReviewMessage:
        """Review code for best practices and maintainability"""
        
        prompt = f"""You are a senior software engineer reviewing code quality. Analyze this {message.language} code:

```{message.language}
{message.code_snippet}
```

Evaluate:
1. Code readability and clarity
2. Naming conventions
3. Error handling
4. Code duplication (DRY principle)
5. Single Responsibility Principle
6. Testing considerations
7. Documentation quality

Respond ONLY with valid JSON in this exact format (no additional text):
{{
  "findings": [
    {{
      "type": "best-practice",
      "severity": "low",
      "issue": "Poor variable naming",
      "line": "3",
      "recommendation": "Use descriptive variable names like 'user_count' instead of 'x'"
    }}
  ],
  "severity_score": 3
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
                "type": "best-practice",
                "severity": "low",
                "issue": "Code quality analysis completed but response formatting error occurred",
                "line": "N/A",
                "recommendation": "Manual code review recommended"
            })
        
        message.from_agent = self.agent_id
        return message

