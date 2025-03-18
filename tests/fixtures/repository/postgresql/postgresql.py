"""Automatically truncate all tables before each test."""

import pytest

from app.internal.repository.v1.postgresql import connection


async def __clean_postgres():
    """Truncate all tables (except specified ones) before each test."""

    q = """
        SELECT 'TRUNCATE TABLE ' || string_agg(quote_ident(tablename), ', ') || ' CASCADE;' AS truncate_statement
        FROM pg_tables
        WHERE schemaname = 'public'
            AND tablename NOT LIKE '%yoyo%'
            AND tablename NOT IN ('user_roles', 'media_type', 'project_type', 'font_extension');
    """

    async with connection.get_connection(return_pool=True) as pool:
        async with connection.acquire_connection(pool) as cursor:
            await cursor.execute(q)
            result = await cursor.fetchone()
            truncate_statement = result["truncate_statement"]

            if truncate_statement:
                await cursor.execute(truncate_statement)


@pytest.fixture(autouse=True, scope="function")
async def auto_clean_postgres():
    """Automatically clean postgres before each test module."""

    await __clean_postgres()


@pytest.fixture()
async def clean_postgres():
    """Clean postgres."""
    await __clean_postgres()
