"""Tests for the Sentinel CLI wake-call flow."""

import unittest
from unittest.mock import patch

import main


class MainWakeCallTests(unittest.TestCase):
    @patch("main.input", side_effect=["not sentinel", "Hey Sentinel", "exit"])
    @patch("main.SentinelAgent")
    def test_wake_call_required_before_authentication(self, mock_agent, mock_input):
        agent = mock_agent.return_value
        agent.check_wake_call.side_effect = lambda text: text.casefold() == "hey sentinel"
        agent.authenticate_fallback_from_environment.return_value = True
        agent.handle_request.side_effect = lambda request: f"handled: {request}"

        main.main()

        self.assertEqual(agent.check_wake_call.call_count, 2)
        agent.authenticate_fallback_from_environment.assert_called_once_with()
        self.assertEqual(agent.handle_request.call_count, 0)


if __name__ == "__main__":
    unittest.main()
