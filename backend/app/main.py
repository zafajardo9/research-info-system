import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import db


origins= [
    "*"
]

app = FastAPI(
        title= "PUP-RIZ",
        description= "Research Information System",
        version= "1.3",
)

def init_app():
    db.init()

    global app

    # app = FastAPI(
    #     title= "PUP-RIZ",
    #     description= "Login Student Page",
    #     version= "1",
    # )

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

    from app.controller import authentication, users, research_controller, auth_controller, admin_power, comment, adviser_controller, ethics, manuscript_controller, copyright_controller, all_about_info

    app.include_router(authentication.router)
    app.include_router(users.router)
    app.include_router(all_about_info.router)
    app.include_router(research_controller.router)
    app.include_router(auth_controller.router)
    app.include_router(adviser_controller.router)
    app.include_router(admin_power.router)
    app.include_router(comment.router)
    app.include_router(ethics.router)
    app.include_router(manuscript_controller.router)
    app.include_router(copyright_controller.router)


    return app


app = init_app()

def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host= "0.0.0.0", port=8888, reload=True)
    #uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)