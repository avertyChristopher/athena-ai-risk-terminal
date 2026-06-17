import os
from pathlib import Path

TEST_DATABASE = Path(__file__).resolve().parents[1] / "athena_test.db"

os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{TEST_DATABASE.as_posix()}"

if TEST_DATABASE.exists():
    TEST_DATABASE.unlink()
