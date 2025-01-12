from fastapi import HTTPException
from pymongo import MongoClient
from bson import ObjectId
import os

def load_doctors():
    client = MongoClient(os.getenv("MONGODB_URI"))
    database = client.get_database("hospital-management")
    __doctors = database.get_collection("doctors")
    
    return __doctors

async def add_doctor(request):
    try:
        __doctors = load_doctors()
        doctor_info = await request.json()
        created_doctor = __doctors.insert_one(doctor_info)
        
        if created_doctor.inserted_id is None:
            print("Doctor is not created")
            return {
                "success": False,
                "message": "Doctor is not created",
                "data": []
            }
        print("Doctor is created")
        res = {
            "success": True,
            "message": "Doctor created successfully",
            "data": str(created_doctor.inserted_id)
        }
        return res

    except Exception as e:
        return {
            "success": False,
            "message": e,
            "data": []
        }

def get_doctor():
    try:
        __doctors = load_doctors()
        doctors = __doctors.find()
        
        new_doctors = []
        for item in doctors:
            item['_id'] = str(item['_id'])
            new_doctors.append(item)
        
        if len(new_doctors) <= 0:
            print("Doctors are not found")
            return {
                "success": False,
                "message": "Doctors are not found",
                "data": []
            }
        print("Doctors are found")
        res = {
            "success": True,
            "message": "Doctors are found successfully",
            "data": new_doctors
        }
        return res

    except Exception as e:
        return {
            "success": False,
            "message": e,
            "data": []
        }

async def update_doctor(request, id):
    try:
        __doctors = load_doctors()
   
        data_to_update = await request.json()

        # Retrieve the doctor document from the collection
        query_filter = {'_id': ObjectId(id)}
        update_operation = { '$set': data_to_update }
        __doctors.update_one(query_filter, update_operation)
    
        return {
            "success": True,
            "message": "Doctor data updated successfully",
        }

    except Exception as e:
        return {
            "success": False,
            "message": e,
            "data": []
        }

def delete_doctor(id):
    try:
        __doctors = load_doctors()
        
        __doctors.delete_one({'_id': ObjectId(id)})
    
        return {
            "success": True,
            "message": "Doctor data deleted successfully",
            "data": []
        }

    except Exception as e:
        return {
            "success": False,
            "message": e,
            "data": []
        }
