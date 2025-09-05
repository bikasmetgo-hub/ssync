import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# Import your models' Base class here
from app.db.base import Base
from app.models.user import User  # noqa: F401 - This import is needed for alembic to detect the model
from app.models.social_account import SocialAccount  # noqa: F401 - This import is needed for alembic to detect the model
from app.models.organization import Organization  # noqa: F401 - This import is needed for alembic to detect the model
from app.models.organization_member import OrganizationMember  # noqa: F401 - This import is needed for alembic to detect the model
from app.models.invite import Invite  # noqa: F401 - This import is needed for alembic to detect the model
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Get database URL from environment variable or fall back to alembic.ini
    url = os.getenv("DATABASE_URL")
    if url is None:
        url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # Get database URL from environment variable or fall back to alembic.ini
    database_url = os.getenv("DATABASE_URL")
    if database_url is None:
        database_url = config.get_section(config.config_ini_section, {}).get("sqlalchemy.url")

    configuration = config.get_section(config.config_ini_section, {})
    if database_url:
        configuration["sqlalchemy.url"] = database_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
