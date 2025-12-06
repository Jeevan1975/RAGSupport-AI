from fastapi import APIRouter, HTTPException
from ..models.schemas import SignupRequest, LoginRequest
from ..database.supabase_client import supabase


router = APIRouter()


# User signup endpoint
@router.post("/signup")
async def signup(request: SignupRequest):
    
    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
        return {
            "message": "Signup successfull. Check your email to verify your account.",
            "data": response
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    

# User login endpoint
@router.post("/login")
async def login(request: LoginRequest):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        if not response:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        session = response.session
        
        return {
            "message": "Login successfull",
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "user": session.user
        }
    
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid email or password")