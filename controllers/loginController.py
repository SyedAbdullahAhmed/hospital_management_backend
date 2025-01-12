from fastapi import HTTPException
from pymongo import MongoClient
import json
from bson import ObjectId
import os



def load_admins():
    uri = os.getenv("MONGODB_URI")
    client = MongoClient(uri)
    database = client.get_database("hospital-management")
    __admins = database.get_collection("admins")
    
    return __admins

async def admin_login(request):
    try:
        __admins=load_admins()
        data= await request.json()
        username=data['name']
        password=data['password']
        
        print(username,password)
        
        if not username or not password or len(username) < 3 or len(password) < 8:
            raise HTTPException(status_code=400, detail="Invalid username or password")
        
        admin = __admins.find_one({'name': username,'password':password})
        

        if admin is None:
            return {
                "success": False,
                "message": "Admin not found",
                "data": []
            }
        
        admin['_id'] = str(admin['_id'])
        
        return {
            "success": True,
            "message": "User data found successfully",
            "data": admin
        }
    except Exception as e:
         return {
            "success": False,
            "message": e,
            "data": []
        }
    

async def add_admin(request): 
    try:
        __admins=load_admins()
        admin_info= await request.json()
        created_admin = __admins.insert_one(admin_info)
        
        if created_admin.inserted_id == None:
            print("Admin is not created")
            return {
                "success": False,
                "message": "Admin is not created",
                "data": []
            }
        print("Admin is created")
        res={
            "success": True,
            "message": "Admin created successfully",
            "data": str(created_admin.inserted_id)
        }
        return res

    except Exception as e:
        print("Admin is not created")
        raise HTTPException(status_code=500, detail=f"Some error occurred:{e}")
