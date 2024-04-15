from fastapi import FastAPI, Form, HTTPException, Query, UploadFile, File, status
from typing import Optional
from pydantic import BaseModel
from datetime import date
from uuid import uuid4
import os
import sqlite3
import Pyro4

ns = Pyro4.locateNS()
uri = ns.lookup("supernode")
supernode = Pyro4.Proxy(uri)

app = FastAPI()

conn = sqlite3.connect("medical_files.sqlite")
c = conn.cursor()

# Create table if not exists
c.execute("""CREATE TABLE IF NOT EXISTS medical_files
             (id INTEGER PRIMARY KEY AutoIncrement,
             name TEXT,
             patient_id TEXT,
             dob DATE,
             disease TEXT,
             treatment TEXT,
             doctor TEXT,
             medication TEXT,
             diagnosis_date DATE,
             discharge_date DATE,
             hospital_record_id TEXT,
             was_admitted INTEGER,
             file_address TEXT)""")
conn.commit()


class MedicalFile(BaseModel):
    name: str
    patient_id: str
    dob: date
    disease: str
    treatment: str
    doctor: str
    medication: str
    diagnosis_date: date
    discharge_date: Optional[date]
    hospital_record_id: str
    was_admitted: bool


# Function to generate a unique ID for each medical file
def generate_file_id():
    return str(uuid4())


# Function to save file to the specified address
def save_file(file_data: UploadFile):
    file_id = generate_file_id()
    file_name = f"{file_id}_{file_data.filename}"
    supernode.upload_file(file_name, file_data.file.read())
    return file_name


# Add a medical file
@app.post("/files/")
async def add_file(
    name: str = Form,
    patient_id: str = Form,
    dob: date = Form,
    disease: str = Form,
    treatment: str = Form,
    doctor: str = Form,
    medication: str = Form,
    diagnosis_date: date = Form,
    discharge_date: Optional[date] = Form,
    hospital_record_id: str = Form,
    was_admitted: bool = Form,
    file_data: UploadFile = File(...),
):
    file_address = save_file(file_data)

    c.execute(
        """INSERT INTO medical_files ( name, patient_id, dob, disease, treatment, doctor, medication, diagnosis_date, discharge_date, hospital_record_id, was_admitted, file_address)
                 VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            name,
            patient_id,
            dob,
            disease,
            treatment,
            doctor,
            medication,
            diagnosis_date,
            discharge_date,
            hospital_record_id,
            int(was_admitted),
            file_address,
        ),
    )
    conn.commit()
    return {"success": True}


# # Delete a medical file
# @app.delete("/files/{file_id}")
# async def delete_file(file_id: str):
#     c.execute("SELECT file_address FROM medical_files WHERE id=?", (file_id,))
#     file_address = c.fetchone()
#     if not file_address:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
#         )
#     os.remove(file_address[0])  # Remove the file from the filesystem
#     c.execute("DELETE FROM medical_files WHERE id=?", (file_id,))
#     conn.commit()
#     return {"message": "File deleted successfully"}


# # Get a medical file by ID
# @app.get("/files/{file_id}")
# async def get_file(file_id: str):
#     c.execute("SELECT * FROM medical_files WHERE id=?", (file_id,))
#     file_data = c.fetchone()
#     if not file_data:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
#         )
#     return MedicalFile(
#         id=file_data[0],
#         name=file_data[1],
#         patient_id=file_data[2],
#         dob=file_data[3],
#         disease=file_data[4],
#         treatment=file_data[5],
#         doctor=file_data[6],
#         medication=file_data[7],
#         diagnosis_date=file_data[8],
#         discharge_date=file_data[9],
#         hospital_record_id=file_data[10],
#         was_admitted=bool(file_data[11]),
#         file_address=file_data[12],
#     )


# # Search for medical files by patient ID
# @app.get("/files/")
# async def search_files(
#     patient_id: Optional[str] = Query(None, min_length=1, max_length=50),
# ):
#     if not patient_id:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Patient ID is required"
#         )
#     c.execute("SELECT * FROM medical_files WHERE patient_id=?", (patient_id,))
#     found_files = c.fetchall()
#     if not found_files:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No files found for the patient ID",
#         )
#     return [
#         MedicalFile(
#             id=file_data[0],
#             name=file_data[1],
#             patient_id=file_data[2],
#             dob=file_data[3],
#             disease=file_data[4],
#             treatment=file_data[5],
#             doctor=file_data[6],
#             medication=file_data[7],
#             diagnosis_date=file_data[8],
#             discharge_date=file_data[9],
#             hospital_record_id=file_data[10],
#             was_admitted=bool(file_data[11]),
#             file_address=file_data[12],
#         )
#         for file_data in found_files
#     ]
