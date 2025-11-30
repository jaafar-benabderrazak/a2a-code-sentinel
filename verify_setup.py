"""
Verification script to ensure all components are properly imported
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("🔍 Verifying A2A Code Review System...\n")

# Test 1: Import messaging
print("1️⃣ Testing messaging module...")
try:
    from messaging.message import CodeReviewMessage
    print("   ✅ CodeReviewMessage imported successfully")
except Exception as e:
    print(f"   ❌ Failed to import CodeReviewMessage: {e}")
    sys.exit(1)

# Test 2: Import agents
print("\n2️⃣ Testing agents module...")
try:
    from agents.security_agent import SecurityReviewAgent
    from agents.performance_agent import PerformanceReviewAgent
    from agents.best_practices_agent import BestPracticesAgent
    from agents.orchestrator import CodeReviewOrchestrator
    print("   ✅ All agent classes imported successfully")
except Exception as e:
    print(f"   ❌ Failed to import agents: {e}")
    sys.exit(1)

# Test 3: Create message instance
print("\n3️⃣ Testing message creation...")
try:
    from datetime import datetime
    message = CodeReviewMessage(
        id="test-123",
        from_agent="test",
        to_agent="security",
        code_snippet="print('hello')",
        language="python"
    )
    print(f"   ✅ Message created: {message.id}")
except Exception as e:
    print(f"   ❌ Failed to create message: {e}")
    sys.exit(1)

# Test 4: Create agent instances
print("\n4️⃣ Testing agent instantiation...")
try:
    security = SecurityReviewAgent()
    performance = PerformanceReviewAgent()
    best_practices = BestPracticesAgent()
    orchestrator = CodeReviewOrchestrator()
    print(f"   ✅ All agents instantiated")
    print(f"      - Security: {security.agent_id}")
    print(f"      - Performance: {performance.agent_id}")
    print(f"      - Best Practices: {best_practices.agent_id}")
except Exception as e:
    print(f"   ❌ Failed to instantiate agents: {e}")
    sys.exit(1)

# Test 5: Verify orchestrator has all agents
print("\n5️⃣ Testing orchestrator configuration...")
try:
    assert hasattr(orchestrator, 'security_agent')
    assert hasattr(orchestrator, 'performance_agent')
    assert hasattr(orchestrator, 'best_practices_agent')
    print("   ✅ Orchestrator properly configured with all agents")
except Exception as e:
    print(f"   ❌ Orchestrator configuration error: {e}")
    sys.exit(1)

# Test 6: Verify examples exist
print("\n6️⃣ Testing examples...")
try:
    examples = [
        project_root / "examples" / "vulnerable_code_example.py",
        project_root / "examples" / "performance_issues_example.py",
        project_root / "examples" / "maintainability_example.py",
    ]
    for example in examples:
        if not example.exists():
            raise FileNotFoundError(f"Missing: {example.name}")
    print(f"   ✅ All {len(examples)} example files exist")
except Exception as e:
    print(f"   ❌ Example files error: {e}")
    sys.exit(1)

# Test 7: Verify tests exist
print("\n7️⃣ Testing test files...")
try:
    test_file = project_root / "tests" / "test_agents.py"
    if not test_file.exists():
        raise FileNotFoundError("test_agents.py not found")
    print("   ✅ Test file exists")
except Exception as e:
    print(f"   ❌ Test files error: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("✅ ALL VERIFICATION CHECKS PASSED!")
print("="*70)
print("\n📋 Project Structure:")
print("   ├── agents/")
print("   │   ├── security_agent.py")
print("   │   ├── performance_agent.py")
print("   │   ├── best_practices_agent.py")
print("   │   └── orchestrator.py")
print("   ├── messaging/")
print("   │   └── message.py")
print("   ├── examples/")
print("   │   ├── vulnerable_code_example.py")
print("   │   ├── performance_issues_example.py")
print("   │   └── maintainability_example.py")
print("   └── tests/")
print("       └── test_agents.py")

print("\n🚀 Ready to use! Try:")
print("   python main.py")
print("   python examples/vulnerable_code_example.py")
print("   pytest tests/")

