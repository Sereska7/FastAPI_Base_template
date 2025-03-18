"""cities."""

from yoyo import step

__depends__ = {"20231112_10_wPUeW-countries"}

steps = [
    step(
        """
            create table if not exists city(
                city_id serial primary key,
                country_id int not null references country,
                city_name text not null unique,
                city_code text not null unique,
                constraint unique_country_and_city_code unique (country_id, city_code)
            );
        """,
        """
            drop table if exists city cascade;
        """
    )
]
