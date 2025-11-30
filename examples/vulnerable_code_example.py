"""Example 1: Code with security vulnerabilities"""

import asyncio
from agents.orchestrator import CodeReviewOrchestrator


async def example_vulnerable_code():
    """Example 1: Code with security vulnerability"""
    
    code = """
def get_user_data(user_id):
    # Vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)

def render_comment(comment):
    # Vulnerable to XSS
    return f"<div>{comment}</div>"
    
@app.route('/api/data')
def get_data():
    # Missing authentication
    data = load_sensitive_data()
    return jsonify(data)
"""
    
    orchestrator = CodeReviewOrchestrator()
    report = await orchestrator.review_code(code, "python")
    
    print("\n" + "="*70)
    print("CODE REVIEW REPORT: Vulnerable Code Example")
    print("="*70)
    print(f"\nStatus: {report['summary']['status']}")
    print(f"Severity Score: {report['summary']['severity_score']}/10")
    print(f"\n📊 Issues Found:")
    print(f"   🔴 Critical: {report['summary']['critical']}")
    print(f"   🟡 Warnings: {report['summary']['warnings']}")
    print(f"   🔵 Suggestions: {report['summary']['suggestions']}")
    
    if report['findings']['critical']:
        print(f"\n🚨 CRITICAL ISSUES - BLOCKING MERGE:")
        for finding in report['findings']['critical']:
            print(f"\n   Issue: {finding['issue']}")
            print(f"   Line: {finding['line']}")
            print(f"   Fix: {finding['recommendation']}")


if __name__ == "__main__":
    asyncio.run(example_vulnerable_code())

