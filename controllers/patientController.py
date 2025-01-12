from fastapi import HTTPException
from pymongo import MongoClient
from bson import ObjectId
import os

def load_patients():
    client = MongoClient(os.getenv("MONGODB_URI"))
    database = client.get_database("hospital-management")
    __patients = database.get_collection("patients")
    
    return __patients

async def add_patient(request):
    try:
        __patients=load_patients()
        patient_info= await request.json()
        created_patient = __patients.insert_one(patient_info)
        
        if created_patient.inserted_id == None:
            print("Patient is not created")
            return {
                "success": False,
                "message": "Patient is not created",
                "data": []
            }
        print("Patient is created")
        res={
            "success": True,
            "message": "Patient created successfully successfully",
            "data": str(created_patient.inserted_id)
        }
        return res

    except Exception as e:
        {
            "success": False,
            "message": e,
            "data": []
        }

def get_patient():
    try:
        __patients=load_patients()
        patients = __patients.find()
        
        new_patients=[]
        for item in patients:
            item['_id'] =str(item['_id'])
            new_patients.append(item)
        
        if len(new_patients) <= 0:
            print("Patients are not found")
            return {
                "success": False,
                "message": "Patients are not found",
                "data": []
            }
        print("Patients are found")
        res={
            "success": True,
            "message": "Patients are found successfully",
            "data": new_patients
        }
        return res

    except Exception as e:
         return {
            "success": False,
            "message": e,
            "data": []
        }

async def update_patient(request,id):
    try:
        __patients=load_patients()
   
        data_to_update=await request.json()

        # Retrieve the user document from the collection
        query_filter = {'_id' : ObjectId(id)}
        update_operation = { '$set' : 
            data_to_update
        }
        __patients.update_one(query_filter,update_operation)
    
        return {
            "success": True,
            "message": "Patient data updated successfully",
        }

    except Exception as e:
         return {
            "success": False,
            "message": e,
            "data": []
        }

def delete_patient(id):
    try:
        __patients=load_patients()
        
        __patients.delete_one({'_id': ObjectId(id)})
    
        return {
            "success": True,
            "message": "Patient data deletd successfully",
            "data": []
        }

    except Exception as e:
        return {
            "success": False,
            "message": e,
            "data": []
        }