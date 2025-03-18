"""country-changelog."""

from yoyo import step

__depends__ = {"20231112_05_knHgl-cities"}

steps = [
    step(
        """
        create table if not exists country_changelog as table country;
    """,
        """
        drop table if exists country_changelog;
    """
    ),
    step(
        """
        alter table country_changelog add column if not exists change_id uuid default gen_random_uuid() primary key;
    """,
        """
        alter table country_changelog drop column if exists change_id;
    """
    )
]
