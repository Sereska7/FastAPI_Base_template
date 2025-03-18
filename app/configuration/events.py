"""Lifespan function."""

import asyncio
from contextlib import asynccontextmanager

from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI

from app.internal.workers import Workers


@inject
@asynccontextmanager
async def lifespan(
    app: FastAPI,
    worker: Worker = Provide[Workers.worker],
):
    app.state.shutting_down = False
    await worker.task()
    worker_task = asyncio.create_task(worker.task())

    yield

    app.state.shutting_down = True
    worker_task.cancel()

    try:
        await worker_task
    except asyncio.CancelledError:
        pass

    await shutdown_event()


async def shutdown_event() -> None:
    pending = [
        task for task in asyncio.all_tasks() if task is not asyncio.current_task()
    ]
    for task in pending:
        task.cancel()

    await asyncio.gather(*pending, return_exceptions=True)
