
import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

from src import main


class TestKaizenFinance(unittest.TestCase):

    def setUp(self):
        """Prepare a clean environment before every test."""
        self.temp_dir = tempfile.TemporaryDirectory()
        main.DATA_FILE = Path(self.temp_dir.name) / "transactions.json"
        main.transactions = []

    def tearDown(self):
        """Clean up temporary test files."""
        self.temp_dir.cleanup()

    def test_add_income(self):
        """Check that income is recorded correctly."""
        with patch("builtins.input", side_effect=["Allowance", "2000"]):
            main.add_transaction("income")

        self.assertEqual(len(main.transactions), 1)
        self.assertEqual(main.transactions[0]["type"], "income")
        self.assertEqual(main.transactions[0]["amount"], 2000.0)

    def test_add_expense(self):
        """Check that expenses are recorded correctly."""
        with patch("builtins.input", side_effect=["Groceries", "350"]):
            main.add_transaction("expense")

        self.assertEqual(len(main.transactions), 1)
        self.assertEqual(main.transactions[0]["type"], "expense")
        self.assertEqual(main.transactions[0]["amount"], 350.0)

    def test_reject_invalid_amount(self):
        """Check that non-numeric amounts are rejected."""
        with patch("builtins.input", side_effect=["Groceries", "abc"]):
            with redirect_stdout(StringIO()) as output:
                main.add_transaction("expense")

        self.assertEqual(len(main.transactions), 0)
        self.assertIn("Invalid amount", output.getvalue())

    def test_reject_negative_amount(self):
        """Check that negative amounts are rejected."""
        with patch("builtins.input", side_effect=["Groceries", "-100"]):
            with redirect_stdout(StringIO()) as output:
                main.add_transaction("expense")

        self.assertEqual(len(main.transactions), 0)
        self.assertIn("greater than zero", output.getvalue())

    def test_reject_empty_description(self):
        """Check that empty descriptions are rejected."""
        with patch("builtins.input", return_value="   "):
            with redirect_stdout(StringIO()) as output:
                main.add_transaction("income")

        self.assertEqual(len(main.transactions), 0)
        self.assertIn("cannot be empty", output.getvalue())

    def test_save_and_load_transactions(self):
        """Check that transactions survive saving and loading."""
        main.transactions = [
            {
                "type": "income",
                "description": "Allowance",
                "amount": 2000.0
            }
        ]

        main.save_transactions()

        main.transactions = []
        main.load_transactions()

        self.assertEqual(len(main.transactions), 1)
        self.assertEqual(main.transactions[0]["description"], "Allowance")

    def test_balance_calculation(self):
        """Check that the financial summary is calculated correctly."""
        main.transactions = [
            {"type": "income", "description": "Allowance", "amount": 2000.0},
            {"type": "income", "description": "Work", "amount": 1500.0},
            {"type": "expense", "description": "Groceries", "amount": 350.0},
            {"type": "expense", "description": "Transport", "amount": 120.0}
        ]

        with redirect_stdout(StringIO()) as output:
            main.view_balance()

        result = output.getvalue()

        self.assertIn("P3500.00", result)
        self.assertIn("P470.00", result)
        self.assertIn("P3030.00", result)


if __name__ == "__main__":
    unittest.main()
