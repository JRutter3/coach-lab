"""
Module containing routines for the lifespan of the API - implementing startup / shutdown
routines e.g.
"""
from contextlib import asynccontextmanager

from config.config_parser import get_config
from database.db_tools import init_db
from fastapi import FastAPI


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    cfg = get_config()
    app.state.db_engine = await init_db(cfg.db_settings)
    yield

    await app.state.db_engine.dispose()