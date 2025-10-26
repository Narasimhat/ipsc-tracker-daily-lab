import contextlib
import sys


def main() -> int:
    """
    Minimal smoke test to verify core dependencies import successfully.
    Returns process exit code (0 = success, 1 = failure).
    """
    print("Running basic import smoke test...")

    try:
        import streamlit  # noqa: F401
        import pandas  # noqa: F401
        import PIL  # noqa: F401
        import db
    except Exception as import_error:  # pragma: no cover - diagnostic path
        print(f"[FAIL] Dependency import failed: {import_error}")
        return 1

    try:
        conn = db.get_conn()
        db.init_db(conn)
        db.ensure_dirs()
    except Exception as db_error:  # pragma: no cover - diagnostic path
        print(f"[FAIL] Database initialization failed: {db_error}")
        return 1
    finally:
        with contextlib.suppress(Exception):
            conn.close()

    print("[OK] Imports and database initialization succeeded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
