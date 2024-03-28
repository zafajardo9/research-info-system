import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.config import db



from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse


origins= [
    "*"
]

app = FastAPI(
        title= "PUP-RIS",
        description= "Research Information System",
        version= "1.5",
)


conf = ConnectionConfig(
    MAIL_USERNAME ="pupris.qc@gmail.com",
    MAIL_PASSWORD = "yqsukxfuzdazeejv", #yqsu kxfu zdaz eejv
    MAIL_FROM = "pupris.qc@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


def init_app():
    db.init()

    global app


    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )



    @app.on_event("startup")
    async def starup():
        await db.create_all()
    
    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    from app.controller import authentication, notif_controller, workflow_controller, prof_process_set, section_controller, announcement_controller, faculty_workflow, student_controller, users, defense_controller, research_professor, research_controller, auth_controller, admin_power, comment, adviser_controller, ethics, manuscript_controller, copyright_controller, all_about_info, FPS_integration

    app.include_router(authentication.router)
    app.include_router(users.router)
    app.include_router(section_controller.router)
    app.include_router(research_controller.router)
    app.include_router(notif_controller.router)
    #app.include_router(auth_controller.router)
    app.include_router(announcement_controller.router)
    app.include_router(student_controller.router)
    app.include_router(faculty_workflow.router)
    app.include_router(workflow_controller.router)
    app.include_router(adviser_controller.router)
    app.include_router(prof_process_set.router)
    app.include_router(research_professor.router)
    app.include_router(admin_power.router)
    app.include_router(comment.router)
    app.include_router(defense_controller.router)
    app.include_router(ethics.router)
    app.include_router(manuscript_controller.router)
    app.include_router(copyright_controller.router)
    app.include_router(all_about_info.router)
    
    # FOR INTEGRATION API
    app.include_router(FPS_integration.router)


    return app


app = init_app()

def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host= "0.0.0.0", port=8888, reload=True)
    # uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)