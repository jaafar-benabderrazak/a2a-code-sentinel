"""Example 2: Code with performance problems"""

import asyncio
from agents.orchestrator import CodeReviewOrchestrator


async def example_performance_issues():
    """Example 2: Code with performance problems"""
    
    code = """
def get_user_posts(user_ids):
    posts = []
    for user_id in user_ids:  # N+1 query problem
        user_posts = db.query(f"SELECT * FROM posts WHERE user_id = {user_id}")
        posts.extend(user_posts)
    return posts

def process_large_file(filename):
    # Loads entire file into memory
    with open(filename) as f:
        data = f.read()  # Could be GBs
        return [line.upper() for line in data.split('\\n')]

def calculate_stats(data):
    # Inefficient algorithm O(n²)
    result = []
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i] == data[j]:
                result.append((i, j))
    return result
"""
    
    orchestrator = CodeReviewOrchestrator()
    report = await orchestrator.review_code(code, "python")
    
    print("\n" + "="*70)
    print("CODE REVIEW REPORT: Performance Issues Example")
    print("="*70)
    print(f"\nStatus: {report['summary']['status']}")
    
    if report['findings']['warnings']:
        print(f"\n⚠️  PERFORMANCE WARNINGS:")
        for finding in report['findings']['warnings']:
            if finding['type'] == 'performance':
                print(f"\n   Issue: {finding['issue']}")
                print(f"   Impact: {finding.get('estimated_impact', 'Significant')}")
                print(f"   Fix: {finding['recommendation']}")


if __name__ == "__main__":
    asyncio.run(example_performance_issues())

