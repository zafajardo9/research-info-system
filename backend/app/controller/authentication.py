from fastapi import APIRouter, HTTPException
from app.schema import EmailSchema, RegisterSchemaFaculty, ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from app.service.auth_service import AuthService, generate_role

#Email
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

from app.main import conf

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



# di naman needed
@router.post("/forgot-password", response_model=ResponseSchema, response_model_exclude_none=True)
async def forgot_password(request_body: ForgotPasswordSchema):
    # Implement forgot password logic
    # Update password for the user
    return ResponseSchema(detail="Password updated successfully!")


@router.get("/integration/authentication", response_model=ResponseSchema)
async def login_faculty():
    token = await AuthService.integration_auth()
    return ResponseSchema(detail="Successfully login", result={"token_type": "Bearer", "access_token": token})


# todo making user automatically register faculty information
# todo integrate with ROBERT

html = """
<p>Thanks for using Fastapi-mail</p> 
"""

@router.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})   