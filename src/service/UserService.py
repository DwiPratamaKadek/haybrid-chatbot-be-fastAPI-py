from src.model.crud.UserCrud import create, getAll, getByName
from core.Request.UserReq import UserRequest
from src.service.AuthService import has_password, verify_password, create_access_token, decode_token
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

class UserService: 

    def create_user(self, req:UserRequest, session=None): 
        if session: 
            data = create(session,{
                "name" : req.name, 
                "password" : has_password(req.password)
            })
        
        return data

    def get_all_user(self, session=None):
        return getAll(session)
    
    def login(self, req:UserRequest, session=None, response=None):
        if not session:
            raise HTTPException(status_code=500, detail="Session not found")
        
        user = getByName(session, req.name)
        
        if not user or not verify_password(req.password, user.password):
             raise HTTPException(status_code=400, detail="Invalid credentials")
        
        token = create_access_token({"user_id":str(user.id)})

        # save token ke cooke
        response.set_cookie(
            key="access_token", 
            value=token, 
            httponly=True,   # tidak bisa diakses JS (aman dari XSS)
            secure=False,    # True kalau pakai HTTPS
            samesite="lax"   # bisa "strict" atau "none"
        )

        return {"access token" : token, "token type":"bearer"}
        

    
    