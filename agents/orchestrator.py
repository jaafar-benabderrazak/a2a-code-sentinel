"""Orchestrator for coordinating multi-agent code reviews"""

import json
import os
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from messaging.message import CodeReviewMessage
from .security_agent import SecurityReviewAgent
from .performance_agent import PerformanceReviewAgent
from .best_practices_agent import BestPracticesAgent


class CodeReviewOrchestrator:
    """Coordinates the multi-agent review process"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.security_agent = SecurityReviewAgent()
        self.performance_agent = PerformanceReviewAgent()
        self.best_practices_agent = BestPracticesAgent()
        self.reports_dir = Path(reports_dir)
        
        # Create reports directory if it doesn't exist
        self.reports_dir.mkdir(exist_ok=True)
        
    async def review_code(
        self, 
        code: str, 
        language: str = "python",
        save_report: bool = True,
        report_name: Optional[str] = None
    ) -> Dict:
        """
        Run code through all review agents
        
        Args:
            code: Code snippet to review
            language: Programming language (default: python)
            save_report: Whether to save report to file (default: True)
            report_name: Optional custom report filename
        
        Returns comprehensive review report
        """
        # Initialize message
        timestamp = datetime.now()
        message = CodeReviewMessage(
            id=f"review-{timestamp.timestamp()}",
            from_agent="orchestrator",
            to_agent="security-agent",
            code_snippet=code,
            language=language
        )
        
        print("🔍 Starting automated code review...\n")
        
        # Pass through each agent in sequence
        print("1️⃣  Security scan...")
        message = await self.security_agent.review(message)
        
        print("2️⃣  Performance analysis...")
        message = await self.performance_agent.review(message)
        
        print("3️⃣  Best practices check...")
        message = await self.best_practices_agent.review(message)
        
        # Generate final report
        report = self._generate_report(message)
        
        # Save report to file if requested
        if save_report:
            report_path = self._save_report(report, timestamp, report_name)
            report['report_file'] = str(report_path)
            
        return report
    
    def _generate_report(self, message: CodeReviewMessage) -> Dict:
        """Generate human-readable report"""
        
        # Categorize findings
        critical = [f for f in message.findings if f['severity'] == 'high']
        warnings = [f for f in message.findings if f['severity'] == 'medium']
        suggestions = [f for f in message.findings if f['severity'] == 'low']
        
        return {
            "summary": {
                "total_issues": len(message.findings),
                "critical": len(critical),
                "warnings": len(warnings),
                "suggestions": len(suggestions),
                "severity_score": message.severity_score,
                "status": "BLOCKED" if critical else "APPROVED_WITH_COMMENTS" if warnings else "APPROVED"
            },
            "findings": {
                "critical": critical,
                "warnings": warnings,
                "suggestions": suggestions
            },
            "code_snippet": message.code_snippet,
            "language": message.language,
            "reviewed_at": message.timestamp.isoformat(),
            "review_id": message.id
        }
    
    def _save_report(self, report: Dict, timestamp: datetime, custom_name: Optional[str] = None) -> Path:
        """Save report to JSON and Markdown files"""
        
        # Generate filename
        if custom_name:
            base_name = custom_name
        else:
            date_str = timestamp.strftime("%Y%m%d_%H%M%S")
            status = report['summary']['status'].lower().replace('_', '-')
            base_name = f"review_{date_str}_{status}"
        
        # Save JSON report
        json_path = self.reports_dir / f"{base_name}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Save Markdown report
        md_path = self.reports_dir / f"{base_name}.md"
        markdown_content = self._generate_markdown_report(report)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"\n💾 Report saved:")
        print(f"   📄 JSON: {json_path}")
        print(f"   📝 Markdown: {md_path}")
        
        return json_path
    
    def _generate_markdown_report(self, report: Dict) -> str:
        """Generate a Markdown-formatted report"""
        
        md = []
        md.append("# Code Review Report")
        md.append("")
        md.append(f"**Review ID**: `{report['review_id']}`  ")
        md.append(f"**Date**: {report['reviewed_at']}  ")
        md.append(f"**Language**: {report['language']}  ")
        md.append(f"**Status**: **{report['summary']['status']}**  ")
        md.append(f"**Severity Score**: {report['summary']['severity_score']}/10")
        md.append("")
        
        # Summary
        md.append("## Summary")
        md.append("")
        md.append(f"- 🔴 **Critical Issues**: {report['summary']['critical']}")
        md.append(f"- 🟡 **Warnings**: {report['summary']['warnings']}")
        md.append(f"- 🔵 **Suggestions**: {report['summary']['suggestions']}")
        md.append(f"- **Total Issues**: {report['summary']['total_issues']}")
        md.append("")
        
        # Critical Issues
        if report['findings']['critical']:
            md.append("## 🚨 Critical Issues")
            md.append("")
            for i, finding in enumerate(report['findings']['critical'], 1):
                md.append(f"### {i}. {finding['issue']}")
                md.append("")
                md.append(f"- **Type**: {finding['type']}")
                md.append(f"- **Severity**: {finding['severity']}")
                md.append(f"- **Line**: {finding.get('line', 'N/A')}")
                md.append(f"- **Recommendation**: {finding['recommendation']}")
                md.append("")
        
        # Warnings
        if report['findings']['warnings']:
            md.append("## ⚠️ Warnings")
            md.append("")
            for i, finding in enumerate(report['findings']['warnings'], 1):
                md.append(f"### {i}. {finding['issue']}")
                md.append("")
                md.append(f"- **Type**: {finding['type']}")
                md.append(f"- **Severity**: {finding['severity']}")
                md.append(f"- **Line**: {finding.get('line', 'N/A')}")
                md.append(f"- **Recommendation**: {finding['recommendation']}")
                md.append("")
        
        # Suggestions
        if report['findings']['suggestions']:
            md.append("## 💡 Suggestions")
            md.append("")
            for i, finding in enumerate(report['findings']['suggestions'], 1):
                md.append(f"### {i}. {finding['issue']}")
                md.append("")
                md.append(f"- **Type**: {finding['type']}")
                md.append(f"- **Severity**: {finding['severity']}")
                md.append(f"- **Line**: {finding.get('line', 'N/A')}")
                md.append(f"- **Recommendation**: {finding['recommendation']}")
                md.append("")
        
        # Code Snippet
        md.append("## Code Reviewed")
        md.append("")
        md.append(f"```{report['language']}")
        md.append(report['code_snippet'].strip())
        md.append("```")
        md.append("")
        
        return "\n".join(md)

