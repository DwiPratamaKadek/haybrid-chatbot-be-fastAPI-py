from src.service.UserService import UserService

from core.Request.UserReq import UserRequest, UserLogin
from fastapi import HTTPException

class UserController:
    def __init__(self):
        self.service = UserService()
    
    def create_user(self, req:UserRequest, session):
        try: 
            result = self.service.create_user(req, session)

            return{
                "status" : "success",
                "data" : result
            }
        except Exception as e: 
            return{
                "status" : "error",
                "data" : str(e)
            }
    
    def get_all_user(self, session):
        try: 
            result = self.service.get_all_user(session)
            return{
                "status" : "success",
                "data" : result
            }
        except Exception as e: 
            return{
                "status" : "error",
                "data" : str(e)
            }
    
    def login(self, req:UserLogin, session, response):
        try: 
            result = self.service.login(req, session, response)
            return{
                "status" : "success",
                "data" : result
            }
        except Exception as e: 
            raise HTTPException(
                status_code=500,
                detail=f"Error: {repr(e)}"
            )