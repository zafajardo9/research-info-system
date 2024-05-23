from app.repository.users import UsersRepository
from fastapi import APIRouter, HTTPException
from app.schema import EmailSchema, RegisterSchemaFaculty, ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from app.service.auth_service import AuthService, generate_role
from fastapi.security import OAuth2PasswordBearer






router = APIRouter(prefix="/auth", tags=['Authentication'])

@router.post("/generate_roles")
async def generate_roles():
    '''WAG NA WAG PIPINDUTIN OR MABABALIW TAYONG LAHAT EMZZZZ'''
    try:
        await generate_role()
        return {"message": "Roles generated successfully"}
    except HTTPException as e:
        return ResponseSchema(detail=f"Error generating role: {str(e)}", result=None)


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



# FOR USER PASSWORD RESET
#user is mag sesend ng email nya then magg sesend ng email sa kanya with token link papunta sa another page for password reset.
# @router.post("/password-reset", response_model=ResponseSchema)
# async def reset_password_user(email: str):
#     token = await AuthService.login_admin(email)
#     return ResponseSchema(detail="Successfully login", result={"token_type": "Bearer", "access_token": token})

# #di ko pa sure to
# @router.get("/reset", response_model=ResponseSchema)
# async def password_reset(request_body: LoginSchema):
#     token = await AuthService.login_admin(request_body)
#     return ResponseSchema(detail="Successfully login", result={"token_type": "Bearer", "access_token": token})


# # sa part na to user will but his new password then if successful rekta sa lofgin page.
# @router.post("/password-reset", response_model=ResponseSchema)
# async def reset_password_user(password: str):
#     token = await AuthService.login_admin(password)
#     return ResponseSchema(detail="Successfully login", result={"token_type": "Bearer", "access_token": token})




# di naman needed
# @router.post("/forgot-password", response_model=ResponseSchema, response_model_exclude_none=True)
# async def forgot_password(request_body: ForgotPasswordSchema):
#     # Implement forgot password logic
#     # Update password for the user
#     return ResponseSchema(detail="Password updated successfully!")


@router.get("/integration/authentication", response_model=ResponseSchema)
async def login_faculty():
    token = await AuthService.integration_auth()
    return ResponseSchema(detail="Successfully login", result={"token_type": "Bearer", "access_token": token})


# todo making user automatically register faculty information
# todo integrate with ROBERT

