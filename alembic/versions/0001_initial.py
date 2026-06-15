"""Initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-15
"""

import geoalchemy2
import sqlalchemy as sa

from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "geodata",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String),
        sa.Column("geom", geoalchemy2.Geometry("GEOMETRY", srid=4326)),
    )


def downgrade():
    op.drop_table("geodata")
