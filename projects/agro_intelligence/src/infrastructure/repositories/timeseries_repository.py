"""
Persistencia de Variable/Observation en Postgres.

Se usa SQLAlchemy Core (tablas + insert/select) en vez de un ORM completo: el modelo es
simple (dos tablas) y no justifica todavía la complejidad de mapear clases con un ORM.
Tampoco se usa Alembic todavía — el esquema se crea con metadata.create_all() y se
versiona con migraciones recién cuando este esquema deje de ser tan chico y estable.
"""

from sqlalchemy import (
    Column,
    Date,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
    select,
)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine

from src.domain.timeseries import Observation, Variable

# Postgres no considera dos NULL iguales para un UNIQUE constraint: si `province` guardara
# NULL para las series nacionales, cada re-ingesta insertaría filas duplicadas en vez de
# actualizar (pasó de verdad: tipo_cambio_a3500 llegó a duplicarse 2x en la primera corrida
# de este fix). Se guarda un sentinel en vez de NULL para que el ON CONFLICT funcione.
NATIONAL_SENTINEL = "NACIONAL"

metadata = MetaData()

variables_table = Table(
    "variables",
    metadata,
    Column("code", String, primary_key=True),
    Column("name", String, nullable=False),
    Column("unit", String, nullable=False),
    Column("vertical", String, nullable=False),
    Column("source", String, nullable=False),
)

observations_table = Table(
    "observations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("variable_code", String, nullable=False),
    Column("province", String, nullable=False),
    Column("date", Date, nullable=False),
    Column("value", Float, nullable=False),
    UniqueConstraint("variable_code", "province", "date", name="uq_observation"),
)


class TimeSeriesRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
        metadata.create_all(engine)

    def upsert_variable(self, variable: Variable) -> None:
        statement = insert(variables_table).values(
            code=variable.code,
            name=variable.name,
            unit=variable.unit,
            vertical=variable.vertical,
            source=variable.source,
        )
        statement = statement.on_conflict_do_update(
            index_elements=["code"],
            set_={
                "name": statement.excluded.name,
                "unit": statement.excluded.unit,
                "vertical": statement.excluded.vertical,
                "source": statement.excluded.source,
            },
        )
        with self.engine.begin() as connection:
            connection.execute(statement)

    def save_observations(self, observations: list[Observation]) -> int:
        if not observations:
            return 0

        rows = [
            {
                "variable_code": observation.variable_code,
                "province": observation.province or NATIONAL_SENTINEL,
                "date": observation.date,
                "value": observation.value,
            }
            for observation in observations
        ]
        statement = insert(observations_table).values(rows)
        statement = statement.on_conflict_do_update(
            index_elements=["variable_code", "province", "date"],
            set_={"value": statement.excluded.value},
        )
        with self.engine.begin() as connection:
            connection.execute(statement)
        return len(rows)

    def load_observations(
        self, variable_code: str, province: str | None = None
    ) -> list[Observation]:
        query = select(observations_table).where(
            observations_table.c.variable_code == variable_code
        )
        if province is not None:
            query = query.where(observations_table.c.province == province)
        query = query.order_by(observations_table.c.date)

        with self.engine.connect() as connection:
            rows = connection.execute(query).all()

        return [
            Observation(
                variable_code=row.variable_code,
                province=None if row.province == NATIONAL_SENTINEL else row.province,
                date=row.date,
                value=row.value,
            )
            for row in rows
        ]
