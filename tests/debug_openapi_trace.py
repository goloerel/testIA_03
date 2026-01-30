from src.main import app
import traceback
import json

def debug_openapi():
    print("Attempting to generate OpenAPI schema...")
    try:
        # This triggers the full generation logic in FastAPI
        schema = app.openapi()
        print("Schema generated successfully in memory.")
        # Try to serialize to JSON to catch encoding errors
        json.dumps(schema)
        print("Schema serialized to JSON successfully.")
    except Exception:
        print("\n--- CRASH DETECTED ---")
        traceback.print_exc()
        print("----------------------\n")

if __name__ == "__main__":
    debug_openapi()
