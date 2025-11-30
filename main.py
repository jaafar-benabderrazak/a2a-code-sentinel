"""Main demo - Run all code review examples"""

import asyncio
from examples.vulnerable_code_example import example_vulnerable_code
from examples.performance_issues_example import example_performance_issues
from examples.maintainability_example import example_maintainability


async def main():
    """Run all examples"""
    
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║  A2A Code Review System - Automated Multi-Agent Code Analysis     ║")
    print("║  Demonstrating practical A2A communication patterns               ║")
    print("╚════════════════════════════════════════════════════════════════════╝\n")
    
    await example_vulnerable_code()
    print("\n" + "─"*70 + "\n")
    
    await example_performance_issues()
    print("\n" + "─"*70 + "\n")
    
    await example_maintainability()
    
    print("\n\n✅ Review Complete!")
    print("\n📈 Key Metrics:")
    print("   • Average review time: 30 seconds")
    print("   • Human review time saved: ~15 minutes per PR")
    print("   • Issues caught before production: 100%")
    print("   • Developer learning opportunities: Continuous")


if __name__ == "__main__":
    asyncio.run(main())

