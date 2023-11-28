from fastapi import APIRouter, HTTPException
from app.schema import RegisterSchemaFaculty, ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from app.service.auth_service import AuthService, generate_role

router = APIRouter(prefix="/auth", tags=['Authentication'])

@router.post("/generate_roles")
async def generate_roles():
    '''WAG NA WAG PIPINDUTIN OR MABABALIW TAYONG LAHAT EMZZZZ'''
    try:
        await generate_role()
        return {"message": "Roles generated successfully"}
    except HTTPException as e:
        return ResponseSchema(detail=f"Error generating role: {str(e)}", result=None)


@router.post("/register/student", response_model=ResponseSchema, response_model_exclude_none=True)
async def register_student(request_body: RegisterSchema):
    await AuthService.register_student(request_body)
    return ResponseSchema(detail="Student registration successful!")

@router.post("/register/faculty", response_model=ResponseSchema, response_model_exclude_none=True)
async def register_faculty(request_body: RegisterSchemaFaculty):
    await AuthService.register_faculty(request_body)
    return ResponseSchema(detail="Faculty registration successful!")

@router.post("/login/student", response_model=ResponseSchema)
async def login_student(request_body: LoginSchema):
    token = await AuthService.login_student(request_body)
    return ResponseSchema(detail="Successfully login", result={"token_type": "Bearer", "access_token": token})

@router.post("/login/faculty", response_model=ResponseSchema)
async def login_faculty(request_body: LoginSchema):
    token = await AuthService.login_faculty(request_body)
    return ResponseSchema(detail="Successfully login", result={"token_type": "Bearer", "access_token": token})


@router.post("/login/admin", response_model=ResponseSchema)
async def login_faculty(request_body: LoginSchema):
    token = await AuthService.login_admin(request_body)
    return ResponseSchema(detail="Successfully login", result={"token_type": "Bearer", "access_token": token})



# di naman needed
@router.post("/forgot-password", response_model=ResponseSchema, response_model_exclude_none=True)
async def forgot_password(request_body: ForgotPasswordSchema):
    # Implement forgot password logic
    # Update password for the user
    return ResponseSchema(detail="Password updated successfully!")


