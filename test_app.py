import requests
import json
import csv
import os
from io import StringIO

# Test configuration
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_health():
    """Test if backend is running and healthy"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def test_frontend_health():
    """Test if frontend is running and accessible"""
    try:
        response = requests.get(FRONTEND_URL)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def test_data_cleaning():
    """Test data cleaning endpoint"""
    # Read sample data
    with open("sample_data.csv", "r") as file:
        csv_content = file.read()
    
    # Prepare request
    files = {"file": ("sample_data.csv", csv_content, "text/csv")}
    data = {"prompt": "Clean this dataset and remove duplicates and noisy entries"}
    
    # Send request
    response = requests.post(f"{BASE_URL}/api/process", data=data, files=files)
    
    if response.status_code == 200:
        result = response.json()
        return "cleaned_data" in result
    return False

def test_data_generation():
    """Test data generation endpoint"""
    # Prepare request
    data = {
        "prompt": "Generate 5 new synthetic data entries based on the schema of a person dataset with Name, Age, City, and Occupation"
    }
    
    # Send request
    response = requests.post(f"{BASE_URL}/api/process", json=data)
    
    if response.status_code == 200:
        result = response.json()
        return "generated_data" in result and len(result["generated_data"]) >= 5
    return False

def test_data_vectorization():
    """Test data vectorization endpoint"""
    # Read sample data
    with open("sample_data.csv", "r") as file:
        csv_content = file.read()
    
    # Prepare request
    files = {"file": ("sample_data.csv", csv_content, "text/csv")}
    data = {"prompt": "Vectorize the text columns in this dataset"}
    
    # Send request
    response = requests.post(f"{BASE_URL}/api/process", data=data, files=files)
    
    if response.status_code == 200:
        result = response.json()
        return "embedding_info" in result
    return False

def test_data_enrichment():
    """Test data enrichment endpoint"""
    # Read sample data
    with open("sample_data.csv", "r") as file:
        csv_content = file.read()
    
    # Prepare request
    files = {"file": ("sample_data.csv", csv_content, "text/csv")}
    data = {"prompt": "Enrich the ambiguous fields in this dataset with relevant context and source links"}
    
    # Send request
    response = requests.post(f"{BASE_URL}/api/process", data=data, files=files)
    
    if response.status_code == 200:
        result = response.json()
        return "enriched_data" in result
    return False

def test_downloads():
    """Test download endpoints"""
    # Test CSV download
    try:
        response = requests.get(f"{BASE_URL}/api/download/csv")
        if response.status_code != 200:
            return False
    except:
        return False
    
    # Test JSON download
    try:
        response = requests.get(f"{BASE_URL}/api/download/json")
        if response.status_code != 200:
            return False
    except:
        return False
    
    # Test FAISS download
    try:
        response = requests.get(f"{BASE_URL}/api/download/faiss")
        if response.status_code != 200:
            return False
    except:
        return False
    
    return True

def run_tests():
    """Run all tests and report results"""
    print("Starting DataSanity application tests...")
    
    # Check if services are running
    backend_healthy = test_backend_health()
    print(f"Backend health check: {'PASS' if backend_healthy else 'FAIL'}")
    
    frontend_healthy = test_frontend_health()
    print(f"Frontend health check: {'PASS' if frontend_healthy else 'FAIL'}")
    
    if not backend_healthy:
        print("\nERROR: Backend is not running. Please start the backend server with 'python backend/main.py'")
        return False
    
    if not frontend_healthy:
        print("\nWARNING: Frontend is not running. The application may still work, but the UI won't be available.")
    
    # Run functional tests
    print("\nRunning functional tests...")
    
    cleaning_result = test_data_cleaning()
    print(f"Data cleaning test: {'PASS' if cleaning_result else 'FAIL'}")
    
    generation_result = test_data_generation()
    print(f"Data generation test: {'PASS' if generation_result else 'FAIL'}")
    
    vectorization_result = test_data_vectorization()
    print(f"Data vectorization test: {'PASS' if vectorization_result else 'FAIL'}")
    
    enrichment_result = test_data_enrichment()
    print(f"Data enrichment test: {'PASS' if enrichment_result else 'FAIL'}")
    
    downloads_result = test_downloads()
    print(f"Download endpoints test: {'PASS' if downloads_result else 'FAIL'}")
    
    # Summary
    all_passed = all([
        backend_healthy, cleaning_result, generation_result,
        vectorization_result, enrichment_result, downloads_result
    ])
    
    print("\n" + "=" * 50)
    print(f"TEST SUMMARY: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("=" * 50)
    
    if all_passed:
        print("\n🎉 DataSanity application is fully functional!")
        print("You can now use the application by visiting http://localhost:3000")
        print("\nTo start the application:")
        print("1. Start the backend: cd backend && python main.py")
        print("2. Start the frontend: cd frontend && npm run dev")
    else:
        print("\n❌ Some tests failed. Please check the application setup and try again.")
        print("Refer to SETUP.md for installation instructions.")
    
    return all_passed

if __name__ == "__main__":
    run_tests()
