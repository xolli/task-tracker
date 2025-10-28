from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool

from alembic import context

# Import SQLModel metadata
from sqlmodel import SQLModel
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata for 'autogenerate' support

target_metadata = SQLModel.metadata

# Optionally, allow URL override via env var DATABASE_URL to keep single source of truth
section = config.get_section(config.config_ini_section)
if section is None:
    section = {}
url = os.getenv("DATABASE_URL") or section.get("sqlalchemy.url")
if url:
    section["sqlalchemy.url"] = url
    config.set_section_option(config.config_ini_section, "sqlalchemy.url", url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    """

    url = config.get_main_option("sqlalchemy.url")
    is_sqlite = url.startswith("sqlite") if url else False
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        render_as_batch=is_sqlite,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    configuration = config.get_section(config.config_ini_section)
    assert configuration is not None

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Detect SQLite to enable batch mode which emulates ALTER via copy-and-move
        url = configuration.get("sqlalchemy.url") if configuration else None
        is_sqlite = url.startswith("sqlite") if url else False
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            render_as_batch=is_sqlite,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
