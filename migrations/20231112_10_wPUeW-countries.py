"""countries."""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            create table if not exists country(
                country_id serial primary key,
                country_name text not null unique,
                country_code text not null unique
            );
        """,
        """
            drop table if exists country cascade;
        """
    )
]
