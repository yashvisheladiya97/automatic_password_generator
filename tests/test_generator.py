import unittest
from generator import generate_password


class GeneratorTests(unittest.TestCase):
    def test_length(self):
        self.assertEqual(len(generate_password(20)), 20)

    def test_selected_classes_present(self):
        password = generate_password(
            16, uppercase=True, lowercase=False, digits=True, symbols=False
        )
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertFalse(any(c.islower() for c in password))
        self.assertFalse(any(not c.isalnum() for c in password))

    def test_no_classes_rejected(self):
        with self.assertRaises(ValueError):
            generate_password(12, uppercase=False, lowercase=False, digits=False, symbols=False)

    def test_minimum_length(self):
        with self.assertRaises(ValueError):
            generate_password(7)


if __name__ == "__main__":
    unittest.main()
