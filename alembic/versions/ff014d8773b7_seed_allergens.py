"""seed allergens

Revision ID: ff014d8773b7
Revises: c9ed78e51a60
Create Date: 2026-11-05 12:36:36.645460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff014d8773b7'
down_revision: Union[str, Sequence[str], None] = 'c9ed78e51a60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ---- added: the data this migration inserts ----
ALLERGENS = ["peanut", "tree_nut", "dairy", "egg", "gluten", "soy", "fish", "shellfish", "sesame"]

allergen_table = sa.table("allergen", sa.column("name", sa.Text))


def upgrade() -> None:
    """Insert the standard allergen list."""
    op.bulk_insert(allergen_table, [{"name": name} for name in ALLERGENS])


def downgrade() -> None:
    """Remove the allergens this migration added."""
    op.execute(allergen_table.delete().where(allergen_table.c.name.in_(ALLERGENS)))