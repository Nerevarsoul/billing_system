import logging

import uvicorn
from fastapi import FastAPI

from app.billing.views import account_router
from app.db import database
from app.utils import parse_args


logger = logging.getLogger(__name__)


app = FastAPI()
app.include_router(account_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


def main():
    options = parse_args()
    logger.info("Server start")
    uvicorn.run(app, host=options.host, port=options.port)


if __name__ == "__main__":
    main()
