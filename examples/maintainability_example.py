"""Example 3: Code quality issues"""

import asyncio
from agents.orchestrator import CodeReviewOrchestrator


async def example_maintainability():
    """Example 3: Code quality issues"""
    
    code = """
def f(x, y, z):  # Poor naming
    a = x + y
    b = a * z
    c = b / 2
    if c > 100:
        return True
    else:
        return False  # Unnecessary else

def process_data(data):
    # No error handling
    result = expensive_operation(data)
    return result

# Duplicated code
def get_active_users():
    return db.query("SELECT * FROM users WHERE active = 1")

def get_inactive_users():
    return db.query("SELECT * FROM users WHERE active = 0")
"""
    
    orchestrator = CodeReviewOrchestrator()
    report = await orchestrator.review_code(code, "python")
    
    print("\n" + "="*70)
    print("CODE REVIEW REPORT: Code Quality Example")
    print("="*70)
    
    if report['findings']['suggestions']:
        print(f"\n💡 CODE QUALITY SUGGESTIONS:")
        for finding in report['findings']['suggestions']:
            print(f"\n   Issue: {finding['issue']}")
            print(f"   Suggestion: {finding['recommendation']}")


if __name__ == "__main__":
    asyncio.run(example_maintainability())

