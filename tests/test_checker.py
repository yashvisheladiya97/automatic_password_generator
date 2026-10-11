import unittest
from checker import check_password


class CheckerTests(unittest.TestCase):
    def test_empty_password(self):
        self.assertEqual(check_password("").score, 0)

    def test_common_password_is_capped(self):
        self.assertLessEqual(check_password("password").score, 10)

    def test_long_varied_password(self):
        result = check_password("Frosty!River7_Cloud?Amber")
        self.assertGreaterEqual(result.score, 45)

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            check_password(None)


if __name__ == "__main__":
    unittest.main()
