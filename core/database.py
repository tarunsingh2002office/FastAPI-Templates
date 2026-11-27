from datetime import timezone
from bson.codec_options import CodecOptions
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from core.config import db_settings


def mask_uri(uri: str) -> str:
    """The Mongo URI with only the password replaced by ****.

    This is printed at import ON PURPOSE: production and testing get swapped in
    .env, and reading the host back from the logs is how you confirm which one
    this process actually opened before editing anything. Everything that tells
    them apart - scheme, user, host, options - stays readable.

    What must NOT stay readable is the password, because this line lands in the
    container logs, where far more people can read it than can read .env.
    Anything unexpected is hidden rather than printed: a parse surprise must
    never fall back to leaking the raw string.
    """
    try:
        scheme, sep, rest = uri.partition("://")
        if not sep or "@" not in rest:
            return uri                      # no credentials in it at all
        userinfo, _, hostpart = rest.rpartition("@")
        user, has_pwd, _password = userinfo.partition(":")
        if not has_pwd:
            return uri                      # user, but no password
        return f"{scheme}://{user}:****@{hostpart}"
    except Exception:
        return "<MONGODB_URI could not be parsed - hidden>"


# Create a MongoDB client
client = MongoClient(
    db_settings.MONGODB_URI,
    maxPoolSize=100,       # max concurrent connections to Mongo per worker
    minPoolSize=10,        # keep 10 warm
    serverSelectionTimeoutMS=5000
)


print(mask_uri(db_settings.MONGODB_URI))

# Access the default database
db = client.get_database(db_settings.DB_NAME)  # This uses the default database from the URI

# Define collections
users_collection = db.users
UTC_DATES = CodecOptions(tz_aware=True, tzinfo=timezone.utc)
users_collection_utc = users_collection.with_options(codec_options=UTC_DATES)

from pymongo import MongoClient
clientNonAsync = MongoClient(db_settings.MONGODB_URI)
db_non_async = clientNonAsync.get_database(db_settings.DB_NAME)
users_collection_non_async=db_non_async.users
