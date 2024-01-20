from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os


load_dotenv()
DB_CONFIG = os.getenv("DATABASE_URL")
print(DB_CONFIG)
# DB_CONFIG = f"postgresql+asyncpg://pupqc_cloud_user:1r7kf1cJ41wPBAfm88mF77LJNIUuW9jG@dpgcme4jv6n7f5s73f44qi0-a.singapore-postgres.render.com/pupqc_cloud"

# #MAIN
# #postgresql+asyncpg://postgres:fCBCc*G3Ce4geF*c1gFDgB24BCgg234g@viaduct.proxy.rlwy.net:28889/railway
# #SECOND
# #postgresql+asyncpg://postgres:dDbeEdFc54a2dFd1123F3Ab*-GbfEf6g@monorail.proxy.rlwy.net:28241/railway

SECRET_KEY = "zack1234"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600



# Load environment variables from .env file
load_dotenv()

class AsyncDatabaseSession: 

    def __init__(self) -> None:
        self.session = None
        self.engine = None

    def __getattr__(self,name):
        return getattr(self.session,name)

    def init(self):
        #self.engine = create_async_engine(DB_CONFIG, future=True, echo=True)
        self.engine = create_async_engine(DB_CONFIG, future=True, echo=True,pool_size=10, max_overflow=20)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            
    @property
    def is_active(self):
        return self.session.is_active if self.session else False 


db = AsyncDatabaseSession()

async def commit_rollback():
    if db.is_active: 
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        
        
