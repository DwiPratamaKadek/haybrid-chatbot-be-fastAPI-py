from src.model.crud.UserCrud import create, getAll, getById, update, delete
from core.Request.UserReq import UserRequest


class UserService: 

    def create_user(self, req:UserRequest, session=None): 
        if session: 
            data = create(session,{
                "name" : req.name, 
                "password" : req.password
            })
        
        return data

    def get_all_user(self, session=None):
        return getAll(session)