import os
import tempfile
import unittest
from pathlib import Path

from security.env_loader import load_dotenv


class EnvLoaderTests(unittest.TestCase):
    def test_loads_values_without_overwriting_existing_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            path.write_text(
                "# comment\n"
                "SENTINEL_TEST_VALUE=from-file\n"
                "SENTINEL_TEST_QUOTED=\"quoted value\"\n",
                encoding="utf-8",
            )

            os.environ.pop("SENTINEL_TEST_VALUE", None)
            os.environ.pop("SENTINEL_TEST_QUOTED", None)

            load_dotenv(path)

            self.assertEqual(os.environ["SENTINEL_TEST_VALUE"], "from-file")
            self.assertEqual(os.environ["SENTINEL_TEST_QUOTED"], "quoted value")

            os.environ["SENTINEL_TEST_VALUE"] = "existing"
            load_dotenv(path)
            self.assertEqual(os.environ["SENTINEL_TEST_VALUE"], "existing")

    def tearDown(self):
        os.environ.pop("SENTINEL_TEST_VALUE", None)
        os.environ.pop("SENTINEL_TEST_QUOTED", None)


if __name__ == "__main__":
    unittest.main()
