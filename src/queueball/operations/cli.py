import click


@click.group
def cli():
    """A CLI tool for performing periodic maintenance on QueueBall"""


@cli.group("db")
def db_group():
    """The DB group is used for periodic maintenance operations"""


@db_group.command("create-tables")
@click.option("-r", "--recreate", is_flag=True, default=False)
def create_tables_command(*, recreate: bool = False):
    """Create tables in the database.

    Run this command will create tables using SQLAlchemy. This operation will
    only fail if the Models are not defined correctly. If some of the
    tables already exists, it will create the remaining ones.

    Options:
        -r, --recreate: drop the existing tables before creating the new ones
    """
    from queueball.operations import db as db_operations

    if recreate:
        db_operations.drop_tables()
    db_operations.create_tables()


@db_group.command("drop-tables")
def drop_tables_command():
    """Drop tables in the database.

    A shortcut for running this command followed by `create-tables` is to run
    `queueball db create-tables -r`
    """
    from queueball.operations import db as db_operations

    db_operations.drop_tables()
