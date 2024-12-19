"""Simple Flask app to test the Furniture API."""
import requests
from flask import Flask, jsonify

app = Flask(__name__)

BASE_URL = "https://8000-idx-mebel-1734367035391.cluster-rz2e7e5f5ff7owzufqhsecxujc.cloudworkstations.dev/api" 

def get_all_furniture():
    """Get all furniture items from the API."""
    response = requests.get(f"{BASE_URL}/furniture/")
    return response.json()

def get_furniture_detail(furniture_id):
    """Get details of a specific furniture item."""
    response = requests.get(f"{BASE_URL}/furniture/{furniture_id}/")
    return response.json()

@app.route('/test/all')
def test_all_furniture():
    """Test endpoint to get all furniture."""
    try:
        furniture_list = get_all_furniture()
        print("\n=== All Furniture ===")
        for item in furniture_list:
            print(f"\nID: {item['furniture_id']}")
            print(f"Name: {item['name']}")
            print(f"Price: {item['price']} UZS")
            print(f"Images: {len(item['images'])} photos")
            print("-" * 30)
        return jsonify({"status": "success", "data": furniture_list})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/test/detail/<furniture_id>')
def test_furniture_detail(furniture_id):
    """Test endpoint to get furniture details."""
    try:
        furniture = get_furniture_detail(furniture_id)
        print(f"\n=== Furniture Detail: {furniture_id} ===")
        print(f"Name: {furniture['name']}")
        print(f"Description: {furniture['description']}")
        print(f"Price: {furniture['price']} UZS")
        print(f"Video Link: {furniture['video_link']}")
        print(f"Number of Images: {len(furniture['images'])}")
        print("-" * 30)
        return jsonify({"status": "success", "data": furniture})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    print("Starting API test server...")
    print("Available test endpoints:")
    print("1. http://localhost:5000/test/all - Get all furniture")
    print("2. http://localhost:5000/test/detail/<furniture_id> - Get specific furniture details")
    app.run(debug=True)