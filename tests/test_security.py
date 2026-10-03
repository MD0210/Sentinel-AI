import unittest

from security.auth import SecurityManager
from security.policy import AuthorizationPolicy, Role


class SecurityManagerTests(unittest.TestCase):
    def test_success_authenticates_and_resets_failures(self):
        manager = SecurityManager()
        manager.record_failure()
        manager.record_success()
        self.assertTrue(manager.state.authenticated)
        self.assertEqual(manager.state.failed_attempts, 0)

    def test_three_failures_lock_out(self):
        manager = SecurityManager()
        for _ in range(3):
            manager.record_failure()
        self.assertTrue(manager.is_locked())
        self.assertFalse(manager.state.authenticated)

    def test_logout_clears_authentication(self):
        manager = SecurityManager()
        manager.record_success()
        manager.logout()
        self.assertFalse(manager.state.authenticated)


class AuthorizationPolicyTests(unittest.TestCase):
    def test_user_can_request_but_not_admin(self):
        policy = AuthorizationPolicy()
        self.assertTrue(policy.allowed(Role.USER, "request"))
        self.assertFalse(policy.allowed(Role.USER, "admin"))

    def test_admin_can_request_and_admin(self):
        policy = AuthorizationPolicy()
        self.assertTrue(policy.allowed(Role.ADMIN, "request"))
        self.assertTrue(policy.allowed(Role.ADMIN, "admin"))


if __name__ == "__main__":
    unittest.main()
