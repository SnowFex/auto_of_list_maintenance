from sqlalchemy import Table, Column, Integer, String, MetaData


metadata = MetaData()

users = Table(
    "notes",
    metadata,
    Column("address", String, nullable=False),
    Column("floor", Integer, primary_key=True, nullable=False),
    Column("full_name", String, nullable=False),
    Column("position_at_work", String, nullable=False),
    Column("computer_name", String, nullable=False),
    Column("work_group", String, nullable=False),
    Column("comment", String, nullable=True)
)