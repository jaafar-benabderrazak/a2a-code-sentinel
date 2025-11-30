# A2A Mini Project 1: A2A Code Sentinel (Basic Communication)

**Prerequisites**: Basic Python, understanding of async/await

## What You'll Build

**A2A Code Sentinel** – a practical automated code review system that demonstrates A2A (Agent-to-Agent) communication through specialized review agents:

- **Security Agent**: Scans for vulnerabilities (SQL injection, XSS, auth issues)
- **Performance Agent**: Identifies optimization opportunities (N+1 queries, inefficient algorithms)
- **Best Practices Agent**: Reviews code quality (naming, error handling, DRY principle)
- **Orchestrator**: Coordinates the multi-agent review pipeline

## Real-World Value

- ✅ Reduces code review time 
- ✅ Catches security vulnerabilities early
- ✅ Ensures consistent code quality
- ✅ Provides learning opportunities for developers

## Architecture

```
┌──────────────┐
│ Developer    │
│    Code      │
└──────┬───────┘
       │
┌──────▼────────────────────────────────────────┐
│         CodeReviewOrchestrator                │
└───────┬──────────┬──────────┬─────────────────┘
        │          │          │
   ┌────▼───┐ ┌───▼────┐ ┌───▼────────┐
   │Security│ │Perf    │ │Best        │
   │Agent   │ │Agent   │ │Practices   │
   └────┬───┘ └───┬────┘ └───┬────────┘
        │          │          │
        └──────────┴──────────┘
                   │
            ┌──────▼────────┐
            │ Comprehensive │
            │    Report     │
            └───────────────┘
```

## Project Structure

```
a2a-mini-1-basic-communication/
├── README.md
├── agents/
│   ├── __init__.py
│   ├── security_agent.py         # Security vulnerability scanner
│   ├── performance_agent.py      # Performance optimization analyzer
│   ├── best_practices_agent.py   # Code quality reviewer
│   └── orchestrator.py           # Multi-agent coordinator
├── messaging/
│   ├── __init__.py
│   └── message.py                # CodeReviewMessage structure
├── examples/
│   ├── vulnerable_code_example.py      # Security issues demo
│   ├── performance_issues_example.py   # Performance problems demo
│   └── maintainability_example.py      # Code quality issues demo
├── tests/
│   └── test_agents.py
├── main.py                       # Run all examples
├── requirements.txt
└── .env.example
```

## Quick Start

### 1. Install Ollama (Free Local LLM)

**Windows/Mac/Linux**: Download from [ollama.ai](https://ollama.ai/)

Then pull the model:
```bash
ollama pull qwen2.5-coder:7b
```

**📘 See [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for detailed setup instructions**

### 2. Install Python Dependencies

**Option A: Using uv (Recommended - Fast!)**
```bash
# Install uv if you haven't already
pip install uv

# Install dependencies
uv sync

# Or for development with testing tools
uv sync --all-extras
```

**Option B: Using pip**
```bash
pip install -r requirements.txt
```

**Dependencies**:
- `pydantic>=2.0.0` - Data validation
- `python-dotenv>=1.0.0` - Environment config
- `requests>=2.31.0` - Ollama API client

## Author

- **Jaafar Benabderrazak**  
  - Portfolio: [jaafarbenabderrazak.com](https://jaafarbenabderrazak.com/)  
  - LinkedIn: [linkedin.com/in/jaafar-benabderrazak](https://linkedin.com/in/jaafar-benabderrazak)

### 3. Run the Demo

**With uv:**
```bash
# Run all examples
uv run python main.py

# Or run individual examples
uv run python examples/vulnerable_code_example.py
```

**Without uv:**
```bash
# Set PYTHONPATH and run
$env:PYTHONPATH = "$PWD"  # PowerShell
# OR
export PYTHONPATH=$PWD    # Bash/Linux

python main.py
```

**Or use the run script:**
```bash
.\run.ps1  # Windows PowerShell
```

### 💡 Why Ollama?

- ✅ **100% Free** - No API costs ever
- ✅ **Privacy** - Code stays on your machine
- ✅ **No Internet** - Works completely offline
- ✅ **Fast** - Optimized for code analysis

## How It Works

### Message Structure

The `CodeReviewMessage` is passed between agents, accumulating findings:

```python
class CodeReviewMessage(BaseModel):
    id: str
    from_agent: str
    to_agent: str
    code_snippet: str
    language: str
    findings: List[Dict] = []
    severity_score: int = 0
    timestamp: datetime
```

### Agent Communication Flow

1. **Orchestrator** creates initial message with code snippet
2. **Security Agent** scans for vulnerabilities, adds findings
3. **Performance Agent** analyzes efficiency, adds findings
4. **Best Practices Agent** reviews quality, adds findings
5. **Orchestrator** generates comprehensive report

### Example: Security Vulnerabilities

```python
from agents.orchestrator import CodeReviewOrchestrator

code = """
def get_user_data(user_id):
    # Vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
"""

orchestrator = CodeReviewOrchestrator()
report = await orchestrator.review_code(code, "python")

# Report includes:
# - Status: BLOCKED/APPROVED_WITH_COMMENTS/APPROVED
# - Critical issues, warnings, suggestions
# - Specific recommendations for each finding
```

## Key A2A Concepts Demonstrated

### 1. Sequential Agent Pipeline

Agents process the message in sequence, each adding their expertise:

```python
message → Security Agent → Performance Agent → Best Practices Agent → Report
```

### 2. Message Accumulation

Each agent enriches the message with new findings:

```python
# Security agent adds
message.findings.append({
    "type": "security",
    "severity": "high",
    "issue": "SQL injection vulnerability",
    "recommendation": "Use parameterized queries"
})

# Performance agent adds more
message.findings.append({
    "type": "performance",
    "severity": "medium",
    "issue": "N+1 query problem",
    "estimated_impact": "50% reduction in DB calls"
})
```

### 3. Specialized Agents

Each agent has a specific role and expertise:

```python
class SecurityReviewAgent:
    """Expert in finding vulnerabilities"""
    
class PerformanceReviewAgent:
    """Expert in optimization"""
    
class BestPracticesAgent:
    """Expert in code quality"""
```

## Example Output

```
╔════════════════════════════════════════════════════════════════════╗
║  A2A Code Review System - Automated Multi-Agent Code Analysis     ║
╚════════════════════════════════════════════════════════════════════╝

🔍 Starting automated code review...

1️⃣  Security scan...
2️⃣  Performance analysis...
3️⃣  Best practices check...

======================================================================
CODE REVIEW REPORT: Vulnerable Code Example
======================================================================

Status: BLOCKED
Severity Score: 9/10

📊 Issues Found:
   🔴 Critical: 3
   🟡 Warnings: 2
   🔵 Suggestions: 1

🚨 CRITICAL ISSUES - BLOCKING MERGE:

   Issue: SQL injection vulnerability in user_id parameter
   Line: 2-3
   Fix: Use parameterized queries with prepared statements

   Issue: Cross-site scripting (XSS) vulnerability
   Line: 6-7
   Fix: Sanitize user input and use templating engine

   Issue: Missing authentication on sensitive endpoint
   Line: 9-11
   Fix: Add @require_auth decorator
```

## Learning Objectives

After completing this project, you'll understand:

- ✅ **A2A Message Passing**: How agents communicate via structured messages
- ✅ **Agent Specialization**: Creating agents with specific expertise
- ✅ **Sequential Pipelines**: Coordinating multi-agent workflows
- ✅ **Message Enrichment**: How data accumulates across agents
- ✅ **Practical Applications**: Real-world use cases for A2A systems

## Testing

Run tests with pytest:

```bash
pytest tests/
```

Tests cover:
- Individual agent functionality
- Message structure validation
- End-to-end orchestration
- Report generation

## Customization Ideas

### 1. Add More Agent Types

```python
class TypeCheckingAgent:
    """Verify type annotations"""
    
class DocumentationAgent:
    """Check documentation quality"""
    
class TestCoverageAgent:
    """Analyze test coverage"""
```

### 2. Add Parallel Processing

Instead of sequential, process agents in parallel:

```python
results = await asyncio.gather(
    security_agent.review(message),
    performance_agent.review(message),
    best_practices_agent.review(message)
)
```

### 3. Add Severity Configuration

```python
class CodeReviewOrchestrator:
    def __init__(self, severity_threshold: int = 5):
        self.severity_threshold = severity_threshold
        # Block merges if severity_score > threshold
```

### 4. Integrate with CI/CD

```python
# .github/workflows/code-review.yml
- name: Run A2A Code Review
  run: python -m a2a_review --file ${{ github.event.pull_request.diff_url }}
```

## Common Issues & Solutions

### Issue 1: API Rate Limits

**Solution**: Add retry logic with exponential backoff

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
async def review(self, message):
    # API call here
```

### Issue 2: Large Code Files

**Solution**: Split code into chunks

```python
def chunk_code(code: str, max_lines: int = 100):
    lines = code.split('\n')
    return ['\n'.join(lines[i:i+max_lines]) 
            for i in range(0, len(lines), max_lines)]
```

### Issue 3: JSON Parsing Errors

**Solution**: Add error handling

```python
try:
    result = json.loads(response.content[0].text)
except json.JSONDecodeError:
    # Fallback or retry
    result = {"findings": [], "severity_score": 0}
```

## Performance Metrics

- **Average review time**: 15-30 seconds per file (with Ollama)
- **Cost per review**: 🆓 **$0.00 - Completely FREE!**
- **Privacy**: 100% - code never leaves your machine

## Resources

- [Anthropic Messages API](https://docs.anthropic.com/claude/reference/messages_post)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Async Python Guide](https://docs.python.org/3/library/asyncio.html)
- [OWASP Security Guide](https://owasp.org/www-project-top-ten/)

## Production Considerations

Before deploying to production:

1. **Add rate limiting** to prevent API abuse
2. **Implement caching** for repeated code reviews
3. **Add authentication** to protect the API
4. **Set up monitoring** for agent performance
5. **Create fallbacks** for API failures
6. **Add logging** for audit trails
7. **Implement webhook integration** for CI/CD
