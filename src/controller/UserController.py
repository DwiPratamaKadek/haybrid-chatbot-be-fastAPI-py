from src.service.UserService import UserService

from core.Request.UserReq import UserRequest

class UserController:
    def __init__(self):
        self.service = UserService()
    
    def create_user(self, req:UserRequest, session):
        try: 
            result = self.service.create_user(req, session)

            return{
                "status" : "error",
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
                "status" : "error",
                "data" : result
            }
        except Exception as e: 
            return{
                "status" : "error",
                "data" : str(e)
            }