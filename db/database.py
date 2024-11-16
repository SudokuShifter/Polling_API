from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_async_engine(url=DATABASE_URL)
async_session_marker = async_sessionmaker(engine, expire_on_commit=False)
