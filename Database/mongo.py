from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure
from loguru import logger
from pydantic import BaseModel
from settings import settings

class MongoDBConnector:

    _client: AsyncMongoClient | None = None

    @classmethod
    async def connect(cls):
        if cls._client is None:
            
            try:

                connection_options = {
                    "serverSelectionTimeoutMS": 5000,
                    "connectTimeoutMS": 5000,
                    "socketTimeoutMS": 5000,
                    "maxPoolSize": 10,           
                }

                cls._client = AsyncMongoClient(
                    settings.DATABASE_HOST,
                    **connection_options
                )

            except ConnectionFailure as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise
        return cls._client
    
    @classmethod
    async def get_database(cls):
        client = await cls.connect()
        return client[settings.DATABASE_NAME]

    @classmethod
    async def get_collection(cls, collection_name: str):
        db = await cls.get_database()
        return db[collection_name]

    @classmethod
    async def save(cls, collection_name: str, data: BaseModel):
        collection = await cls.get_collection(collection_name)
        await collection.insert_one(data.model_dump())
        logger.info(f"Saved feedback to MongoDB: {data}")
        return cls

    @classmethod
    async def close(cls):
        if cls._client is not None:
            cls._client.close()
            cls._client = None