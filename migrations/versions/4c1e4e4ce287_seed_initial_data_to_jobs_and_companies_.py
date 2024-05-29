"""Seed initial data to jobs and companies tables

Revision ID: 4c1e4e4ce287
Revises: 9aaf8360d2b9
Create Date: 2024-05-29 21:38:12.497797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from lib.seed import create_companies, create_jobs, delete_records


# revision identifiers, used by Alembic.
revision: str = '4c1e4e4ce287'
down_revision: Union[str, None] = '9aaf8360d2b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    delete_records()
    create_companies()
    create_jobs()


def downgrade() -> None:
    delete_records()
