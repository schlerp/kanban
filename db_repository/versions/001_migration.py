from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
project = Table('project', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', Text),
    Column('creator', String(length=64)),
    Column('creation_date', DateTime),
)

task = Table('task', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=64)),
    Column('description', Text),
    Column('creator', String(length=64)),
    Column('creation_date', DateTime),
    Column('owner', String(length=64)),
    Column('owned_date', DateTime),
    Column('completer', String(length=64)),
    Column('complete_date', DateTime),
    Column('project_id', Integer),
    Column('status_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['project'].create()
    post_meta.tables['task'].columns['project_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['project'].drop()
    post_meta.tables['task'].columns['project_id'].drop()
