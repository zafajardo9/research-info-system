from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from dotenv import load_dotenv
import os
import logging

# Load environment variables from a .env file
load_dotenv()

# Database configuration
DB_CONFIG = os.getenv("DATABASE_URL")

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 600))

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Print database configuration for debugging purposes
logger.info(f"Database URL: {DB_CONFIG}")

class AsyncDatabaseSession:
    def __init__(self) -> None:
        self.session: AsyncSession = None
        self.engine = None

    def __getattr__(self, name):
        if self.session is None:
            raise AttributeError(f"'AsyncDatabaseSession' object has no attribute '{name}' because session is not initialized.")
        return getattr(self.session, name)

    async def init(self):
        self.engine = create_async_engine(DB_CONFIG, future=True, echo=True,pool_size=10, max_overflow=20)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    @property
    def is_active(self) -> bool:
        return self.session.is_active if self.session else False

# Instantiate the database session
db = AsyncDatabaseSession()

async def commit_rollback():
    if db.is_active:
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
