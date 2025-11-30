"""Security review agent for finding vulnerabilities"""

import json
import re
from agents.llm_client import OllamaClient
from messaging.message import CodeReviewMessage


class SecurityReviewAgent:
    """Agent specialized in finding security vulnerabilities"""
    
    def __init__(self, model: str = "qwen2.5-coder:7b"):
        self.agent_id = "security-agent"
        self.client = OllamaClient(model=model)
        
    async def review(self, message: CodeReviewMessage) -> CodeReviewMessage:
        """Scan code for security issues"""
        
        prompt = f"""You are a security expert reviewing code. Analyze this {message.language} code for security vulnerabilities:

```{message.language}
{message.code_snippet}
```

Look for:
1. SQL injection vulnerabilities
2. XSS vulnerabilities
3. Authentication/authorization issues
4. Sensitive data exposure
5. Insecure dependencies or APIs
6. CSRF vulnerabilities
7. Input validation issues

Respond ONLY with valid JSON in this exact format (no additional text):
{{
  "findings": [
    {{
      "type": "security",
      "severity": "high",
      "issue": "SQL injection vulnerability in query construction",
      "line": "2-3",
      "recommendation": "Use parameterized queries"
    }}
  ],
  "severity_score": 8
}}

If no issues found, return: {{"findings": [], "severity_score": 0}}"""

        # Get response from Ollama
        response_text = self.client.generate(prompt, max_tokens=2000)
        
        # Parse response (with error handling for non-JSON responses)
        try:
            # Extract JSON from response (in case model adds explanation)
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(response_text)
                
            message.findings.extend(result.get("findings", []))
            message.severity_score = max(message.severity_score, result.get("severity_score", 0))
        except json.JSONDecodeError as e:
            # Fallback if JSON parsing fails
            print(f"⚠️  Warning: Could not parse JSON response from {self.agent_id}")
            print(f"Error: {e}")
            print(f"Raw response: {response_text[:300]}...")
            message.findings.append({
                "type": "security",
                "severity": "low",
                "issue": "Security analysis completed but response formatting error occurred",
                "line": "N/A",
                "recommendation": "Manual security review recommended"
            })
        
        message.from_agent = self.agent_id
        return message

