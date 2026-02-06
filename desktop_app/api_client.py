import requests

BASE_URL = "http://127.0.0.1:8000/api/students/"

# ---------------- CREATE ----------------
def create_student(data):
    url = f"{BASE_URL}add/"
    response = requests.post(url, json=data)
    return response.json()

# ---------------- READ ----------------
def get_students():
    response = requests.get(BASE_URL)
    return response.json()

# ---------------- UPDATE ----------------
def update_student(student_id, data):
    url = f"{BASE_URL}update/{student_id}/"
    response = requests.put(url, json=data)
    return response.json()

# ---------------- DELETE ----------------
def delete_student(student_id):
    url = f"{BASE_URL}delete/{student_id}/"
    response = requests.delete(url)
    return response.status_code

# ---------------- Search ----------------
def search_student(search_entry):
    url = f"{BASE_URL}search/"
    response = requests.get(url, params={"q": search_entry})
    return response.json()

# ---------------- Count ----------------
def count_students():
    url = f"{BASE_URL}count/"
    response = requests.get(url)
    return response.json()["count"]