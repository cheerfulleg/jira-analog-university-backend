from ..config import settings

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": settings.DB_NAME,
                "host": settings.DB_HOST,
                "password": settings.DB_PASS,
                "user": settings.DB_USER,
                "port": settings.DB_PORT,
            },
        }
    },
    "apps": {
        "models": {
            "models": settings.MODELS_LIST + ["aerich.models"],
            "default_connection": "default",
        },
    },
}
