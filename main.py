from fastapi import FastAPI
import logging.config
import logging
import sys
from fastapi import FastAPI
from sqlmodel import Field, SQLModel
import uvicorn
from logging_lib import RouterLoggingMiddleware


# Logging configuration
logging_config = {
    "version": 1,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(process)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)s"
        }
    },
    "handlers": {
        "filehandler": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "json",
            "filename": "api_req_res.log",
            "mode": "a",
            
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "filehandler"
        ],
        "propagate": True
    }
}

logging.config.dictConfig(logging_config)

# Define application
def get_application() -> FastAPI:
    application = FastAPI(title="FastAPI Logging", debug=True)

    return application

# Initialize application
app = get_application()
app.add_middleware(
    RouterLoggingMiddleware,
    logger=logging.getLogger(__name__)
)

# Define SQLModel for testing
class User(SQLModel):
    first_name: str
    last_name: str
    email: str

# Root route that returns a User model
@app.get(
    "/",
    response_model=User,
)
def root():
    user = User(
        first_name="John",
        last_name="Doe",
        email="jon@doe.com"
    )
    return user


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
