# 🆓 Setting Up Free Open-Source LLM with Ollama

This guide will help you set up the code review system using **qwen2.5-coder:7b** - a completely free, open-source LLM running locally on your machine.

## Why Ollama + Qwen2.5-Coder?

- ✅ **100% Free** - No API costs, no usage limits
- ✅ **Privacy** - Everything runs locally, code never leaves your machine
- ✅ **Fast** - Optimized for code analysis and review
- ✅ **No Internet Required** - Works completely offline once downloaded
- ✅ **No API Keys** - Just install and run

## Step 1: Install Ollama

### Windows
1. Download installer from [ollama.ai](https://ollama.ai/)
2. Run the installer
3. Ollama will start automatically

### macOS
```bash
brew install ollama
# or download from https://ollama.ai/
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

## Step 2: Pull the Model

Open a terminal and run:

```bash
# Pull qwen2.5-coder:7b (recommended for code review)
ollama pull qwen2.5-coder:7b
```

This will download ~4.7GB. First time only!

**Alternative models you can try:**
```bash
ollama pull codellama:7b       # 3.8GB - Code-focused
ollama pull llama3.2:3b        # 2GB - Lightweight and fast
ollama pull mistral:7b         # 4.1GB - General purpose
ollama pull deepseek-coder:6.7b # 3.8GB - Code specialist
```

## Step 3: Verify Ollama is Running

Test that Ollama is working:

```bash
# Test the model
ollama run qwen2.5-coder:7b "Write a Python function to calculate fibonacci"

# You should see a code response!
```

To stop the interactive session, type `/bye`

## Step 4: Install Python Dependencies

```bash
cd projects/a2a-mini-1-basic-communication
pip install -r requirements.txt
```

## Step 5: Run the Code Review System

```bash
# Run all examples
python main.py

# Or run individual examples
python examples/vulnerable_code_example.py
python examples/performance_issues_example.py
python examples/maintainability_example.py
```

## 🎯 How It Works

Instead of calling Anthropic's Claude API, the system now:

1. Sends prompts to **Ollama** running locally (`localhost:11434`)
2. Ollama uses **qwen2.5-coder:7b** to analyze the code
3. Responses are parsed and formatted into review reports

## 📊 Performance Comparison

| Aspect | Claude API | Ollama (Local) |
|--------|-----------|----------------|
| **Cost** | ~$0.05-0.15/review | 🆓 Free |
| **Speed** | ~10-20 seconds | ~15-30 seconds |
| **Privacy** | Sent to Anthropic | 🔒 100% Local |
| **Internet** | Required | Not required |
| **Quality** | Excellent | Very Good |

## 🔧 Troubleshooting

### Issue: "Cannot connect to Ollama"

**Solution:**
```bash
# Check if Ollama is running
ollama list

# If not running, start it
ollama serve
```

### Issue: "Model not found"

**Solution:**
```bash
# Make sure the model is downloaded
ollama pull qwen2.5-coder:7b

# List available models
ollama list
```

### Issue: "Response is slow"

**Solutions:**
- Use a smaller model: `ollama pull llama3.2:3b`
- Ensure you have enough RAM (8GB+ recommended)
- Close other memory-intensive applications

### Issue: "JSON parsing errors"

This is normal occasionally with open-source models. The code includes fallback handling:
- Partial findings are still captured
- Manual review suggestions are provided
- System continues to next agent

## 🎛️ Configuration

Create a `.env` file (optional):

```bash
cp .env.example .env
```

Edit `.env` to customize:

```bash
# Use different model
OLLAMA_MODEL=codellama:7b

# Use remote Ollama instance
OLLAMA_BASE_URL=http://192.168.1.100:11434
```

## 🚀 Advanced Usage

### Using Multiple Models

You can use different models for different agents:

```python
from agents.orchestrator import CodeReviewOrchestrator
from agents.security_agent import SecurityReviewAgent
from agents.performance_agent import PerformanceReviewAgent
from agents.best_practices_agent import BestPracticesAgent

# Custom orchestrator with different models
security = SecurityReviewAgent(model="qwen2.5-coder:7b")
performance = PerformanceReviewAgent(model="codellama:7b")
best_practices = BestPracticesAgent(model="llama3.2:3b")
```

### Remote Ollama Instance

Run Ollama on a powerful server and connect from other machines:

```bash
# On server
OLLAMA_HOST=0.0.0.0:11434 ollama serve

# On client
OLLAMA_BASE_URL=http://server-ip:11434 python main.py
```

## 📈 System Requirements

### Minimum
- **RAM**: 8GB
- **Disk**: 10GB free space
- **CPU**: Multi-core processor (4+ cores recommended)

### Recommended
- **RAM**: 16GB+ (for larger models)
- **Disk**: 20GB+ free space
- **GPU**: Optional but speeds up inference significantly

### With GPU (Faster)
Ollama automatically uses GPU if available:
- **NVIDIA**: CUDA support (RTX 20xx series or newer)
- **AMD**: ROCm support
- **Apple**: Metal (M1/M2/M3 chips)

## 🎓 Next Steps

1. **Try different models** to see which works best for your use case
2. **Customize prompts** in the agent files for better results
3. **Fine-tune temperature** settings for more/less creative responses
4. **Add more agents** using the same pattern

## 💡 Pro Tips

1. **Keep Ollama running in background** for faster responses
2. **Warm up models** by running a test query after starting Ollama
3. **Use quantized models** (like :7b) for good balance of speed and quality
4. **Monitor system resources** during reviews
5. **Batch multiple files** for efficient processing

## 🔗 Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Qwen2.5-Coder Model](https://ollama.ai/library/qwen2.5-coder)
- [Available Models](https://ollama.ai/library)
- [Ollama API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)

## ✅ Verification

Test everything is working:

```bash
python verify_setup.py
```

You should see:
```
✅ ALL VERIFICATION CHECKS PASSED!
🚀 Ready to use with Ollama!
```

---

**Enjoy unlimited, free code reviews!** 🎉

No API keys, no costs, complete privacy.

