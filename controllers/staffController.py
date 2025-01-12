from fastapi import HTTPException
from pymongo import MongoClient
from bson import ObjectId
import os

def load_staffs():
    client = MongoClient(os.getenv("MONGODB_URI"))
    database = client.get_database("hospital-management")
    __staffs = database.get_collection("staffs")
    
    return __staffs

async def add_staff(request):
    try:
        __staffs = load_staffs()
        staff_info = await request.json()
        created_staff = __staffs.insert_one(staff_info)
        
        if created_staff.inserted_id == None:
            print("Staff is not created")
            return {
                "success": False,
                "message": "Staff is not created",
                "data": []
            }
        print("Staff is created")
        res = {
            "success": True,
            "message": "Staff created successfully",
            "data": str(created_staff.inserted_id)
        }
        return res

    except Exception as e:
        print("Staff is not created")
        return {
            "success": False,
            "message": e,
            "data": []
        }

def get_staff():
    try:
        __staffs = load_staffs()
        staffs = __staffs.find()
        
        new_staffs = []
        for item in staffs:
            item['_id'] = str(item['_id'])
            new_staffs.append(item)
        
        if len(new_staffs) <= 0:
            print("Staffs are not found")
            return {
                "success": False,
                "message": "Staffs are not found",
                "data": []
            }
        print("Staffs are found")
        res = {
            "success": True,
            "message": "Staffs are found successfully",
            "data": new_staffs
        }
        return res

    except Exception as e:
        return {
            "success": False,
            "message": e,
            "data": []
        }

async def update_staff(request, id):
    try:
        __staffs = load_staffs()
        data_to_update = await request.json()

        # Retrieve the staff document from the collection
        query_filter = {'_id': ObjectId(id)}
        update_operation = { '$set': data_to_update }
        __staffs.update_one(query_filter, update_operation)
    
        return {
            "success": True,
            "message": "Staff data updated successfully",
        }

    except Exception as e:
        return {
            "success": False,
            "message": e,
            "data": []
        }

def delete_staff(id):
    try:
        __staffs = load_staffs()
        __staffs.delete_one({'_id': ObjectId(id)})
    
        return {
            "success": True,
            "message": "Staff data deleted successfully",
            "data": []
        }

    except Exception as e:
        return {
            "success": False,
            "message": e,
            "data": []
        }
