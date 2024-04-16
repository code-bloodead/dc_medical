from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import shutil
import csv
import os
import requests
import threading
from queue import Queue

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary directory to store uploaded files
TEMP_DIR = "temp_files"
# Create temp directory if not exists
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Assuming you have the URL where the FastAPI server is running
API_URL = "http://127.0.0.1:8000/files"

# Function to send the POST request with file data and other fields
def send_post_request(data, file_path):
    # Extracting file name from file_path
    file_name = file_path.split("/")[-1]

    # Creating a dictionary containing query parameters
    query_params = {
        "name": data["name"],
        "patient_id": data["patient_id"],
        "dob": data["dob"],
        "disease": data["disease"],
        "treatment": data["treatment"],
        "doctor": data["doctor"],
        "medication": data["medication"],
        "diagnosis_date": data["diagnosis_date"],
        "discharge_date": data["discharge_date"],
        "hospital_record_id": data["hospital_record_id"],
        "was_admitted": data["was_admitted"],
    }
    
    # Creating a dictionary to pass as files parameter
    files = {'file_data': (file_name, open(file_path, 'rb'))}
    
    # Sending the POST request with query parameters and file data
    response = requests.post(API_URL, params=query_params, files=files)
    
    # Checking the response status
    if response.status_code == 200:
        print("File uploaded successfully.")
    else:
        print("Failed to upload file.")

# Function to process rows from CSV concurrently
# Function to process rows from CSV concurrently
def process_csv_rows(queue):
    while True:
        # Get a row from the queue
        row = queue.get()
        if row is None:  # Check for termination signal
            break
        # Assuming reports are located in 'seed_data/files/report_id'
        file_path = f"seed_data/files/{row['report_file']}"
        send_post_request(row, file_path)
        queue.task_done()

# Reading the CSV file and sending data in POST request
@app.post("/seed")
def seed_file(file: UploadFile = File(...)):
    print("Received file for seeding", file.filename)
     # Save uploaded file to temporary directory
    file_location = f"{TEMP_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Initialize a queue to hold CSV rows
    queue = Queue()

    records = 0

    # Reading CSV file and putting rows into the queue
    with open(file_location, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            queue.put(row)
            records += 1

    # Creating threads to process CSV rows concurrently
    threads = []
    for _ in range(4):  # Maximum of 4 concurrent requests
        thread = threading.Thread(target=process_csv_rows, args=(queue,))
        thread.start()
        threads.append(thread)

    # Wait for all queue tasks to be processed
    queue.join()

    # Signal threads to terminate
    for _ in range(4):
        queue.put(None)

    # Wait for all threads to terminate
    for thread in threads:
        thread.join()

    # All threads have finished processing, so the program can exit
    print("All threads have finished processing.")
    print(f"Seeded {records} records to the server")

    return {
        "success": True,
        "message": f"Seeded {records} records to the server"
    }



# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5002)