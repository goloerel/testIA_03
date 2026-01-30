from fastapi.testclient import TestClient
from src.main import app
import json
import traceback

client = TestClient(app)

def check_openapi():
    print("Checking /openapi.json ...")
    try:
        response = client.get("/openapi.json")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Schema generated successfully.")
            # Verify PUT is in paths
            schema = response.json()
            paths = schema.get("paths", {})
            if "/api/v1/vehicles/{id}" in paths:
                methods = paths["/api/v1/vehicles/{id}"].keys()
                print(f"Methods for /api/v1/vehicles/{{id}}: {list(methods)}")
                if "put" in methods:
                    print("PUT method found in schema.")
                else:
                    print("ERROR: PUT method MISSING in schema.")
            else:
                print("ERROR: Path /api/v1/vehicles/{id} MISSING in schema.")
        else:
            print("Failed to generate schema.")
            print(response.text)
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    check_openapi()
