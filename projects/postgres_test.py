from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "postgresql://postgres:9898@localhost:5432/analytics"
)

query = "SELECT version();"

result = pd.read_sql(query, engine)

print(result)