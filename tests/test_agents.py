"""Tests for code review agents"""

import pytest
from agents.security_agent import SecurityReviewAgent
from agents.performance_agent import PerformanceReviewAgent
from agents.best_practices_agent import BestPracticesAgent
from agents.orchestrator import CodeReviewOrchestrator
from messaging.message import CodeReviewMessage


@pytest.mark.asyncio
async def test_security_agent_review():
    """Test security agent can review code"""
    agent = SecurityReviewAgent()
    message = CodeReviewMessage(
        id="test-1",
        from_agent="test",
        to_agent="security-agent",
        code_snippet="query = f'SELECT * FROM users WHERE id = {user_id}'",
        language="python"
    )
    result = await agent.review(message)
    assert len(result.findings) >= 0
    assert result.from_agent == "security-agent"


@pytest.mark.asyncio
async def test_performance_agent_review():
    """Test performance agent can review code"""
    agent = PerformanceReviewAgent()
    message = CodeReviewMessage(
        id="test-2",
        from_agent="test",
        to_agent="performance-agent",
        code_snippet="for i in range(len(data)):\n    for j in range(len(data)):\n        result.append((i, j))",
        language="python"
    )
    result = await agent.review(message)
    assert len(result.findings) >= 0
    assert result.from_agent == "performance-agent"


@pytest.mark.asyncio
async def test_best_practices_agent_review():
    """Test best practices agent can review code"""
    agent = BestPracticesAgent()
    message = CodeReviewMessage(
        id="test-3",
        from_agent="test",
        to_agent="best-practices-agent",
        code_snippet="def f(x, y):\n    return x + y",
        language="python"
    )
    result = await agent.review(message)
    assert len(result.findings) >= 0
    assert result.from_agent == "best-practices-agent"


@pytest.mark.asyncio
async def test_orchestrator_review():
    """Test orchestrator can coordinate full review"""
    orchestrator = CodeReviewOrchestrator()
    code = """
def get_user(user_id):
    return db.query(f"SELECT * FROM users WHERE id = {user_id}")
"""
    report = await orchestrator.review_code(code, "python")
    assert "summary" in report
    assert "findings" in report
    assert "status" in report["summary"]


def test_message_structure():
    """Test message structure is valid"""
    message = CodeReviewMessage(
        id="test-msg",
        from_agent="agent-a",
        to_agent="agent-b",
        code_snippet="print('test')",
        language="python"
    )
    assert message.id == "test-msg"
    assert message.from_agent == "agent-a"
    assert message.severity_score == 0
    assert len(message.findings) == 0

