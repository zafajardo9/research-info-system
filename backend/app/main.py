import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import db

origins= [
    "http://localhost:5173"
]

def init_app():
    db.init()

    app = FastAPI(
        title= "PUP-RIZ",
        description= "Login Student Page",
        version= "1",
    )

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

    from app.controller import authentication, users, research_paper_controller, auth_controller

    app.include_router(authentication.router)
    app.include_router(users.router)
    app.include_router(research_paper_controller.router)
    app.include_router(auth_controller.router)

    return app

app = init_app()

def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)
   # uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)