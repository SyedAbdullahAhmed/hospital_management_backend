from fastapi import FastAPI,Request,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from pymongo import MongoClient
from bson import ObjectId
import controllers.loginController as loginController
import controllers.patientController as patientController
import controllers.doctorController as doctorController
import controllers.staffController as staffController
from dotenv import load_dotenv

load_dotenv()


uri = os.getenv("MONGODB_URI")

client = MongoClient(uri)
database = client.get_database("hospital-management")
admins = database.get_collection("admins")

app = FastAPI()

origins = [
    "http://localhost:3000", 
    "https://hospital-management-frontend-ten.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Include your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"]   # Allows all headers
)


# admin login
@app.get("/")
async def root():
    return {"name": "Hello"}
# admin login
@app.post("/hospitalManagement/login")
async def root(request: Request):
    return await loginController.admin_login(request)
    
@app.post("/hospitalManagement/addAdmin")
async def root(request:Request):
    return await loginController.add_admin(request)
    
# patient
@app.get("/hospitalManagement/patient")
async def root():
    return patientController.get_patient()

@app.post("/hospitalManagement/patient")
async def root(request:Request):
    return await patientController.add_patient(request)

@app.put("/hospitalManagement/patient/{id}")
async def root(request:Request,id):
    return await patientController.update_patient(request,id)

@app.delete("/hospitalManagement/patient/{id}")
async def root(id):
    return patientController.delete_patient(id)


# doctor
@app.get("/hospitalManagement/doctor")
async def root():
    return doctorController.get_doctor()

@app.post("/hospitalManagement/doctor")
async def root(request: Request):
    return await doctorController.add_doctor(request)

@app.put("/hospitalManagement/doctor/{id}")
async def root(request: Request, id):
    return await doctorController.update_doctor(request, id)

@app.delete("/hospitalManagement/doctor/{id}")
async def root(id):
    return doctorController.delete_doctor(id)

# staff
@app.get("/hospitalManagement/staff")
async def root():
    return staffController.get_staff()

@app.post("/hospitalManagement/staff")
async def root(request: Request):
    return await staffController.add_staff(request)

@app.put("/hospitalManagement/staff/{id}")
async def root(request: Request, id):
    return await staffController.update_staff(request, id)

@app.delete("/hospitalManagement/staff/{id}")
async def root(id):
    return staffController.delete_staff(id)




if __name__ == "__main__": 
    loginController.load_admins()
    patientController.load_patients()
    doctorController.load_doctors()
    print("Server started")
    uvicorn.run(app, host="0.0.0.0", port=4000, reload=True)