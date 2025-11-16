import requests
import json
import os

def test_model_endpoint():
    # Set the base URL for the Flask app
    base_url = "http://localhost:5000"

    # Check if the server is running
    try:
        response = requests.get(base_url)
        assert response.status_code == 200, "Server is not running"
    except requests.exceptions.ConnectionError:
        assert False, "Could not connect to the server"

    # Get the list of available models
    response = requests.get(f"{base_url}/api/models")
    assert response.status_code == 200, "Could not get models"
    models = response.json()
    model_ids = list(models.keys())

    # Test the /api/get_model_response endpoint
    test_data = {
        "prompt": "What is the capital of France?",
        "model_id": model_ids[0]
    }

    response = requests.post(
        f"{base_url}/api/get_model_response",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Check that the response is a JSON object with the expected keys
    response_data = response.json()
    assert "model_name" in response_data, "Response missing 'model_name' key"
    assert "response" in response_data, "Response missing 'response' key"

    print("Test passed!")

if __name__ == "__main__":
    test_model_endpoint()
