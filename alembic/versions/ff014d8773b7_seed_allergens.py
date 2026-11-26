from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'ff014d8773b7'
down_revision: Union[str, Sequence[str], None] = 'c9ed78e51a60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


ALLERGENS = ["peanut", "tree_nut", "dairy", "egg", "gluten", "soy", "fish", "shellfish", "sesame"]

allergen_table = sa.table("allergen", sa.column("name", sa.Text))


def upgrade() -> None:
    op.bulk_insert(allergen_table, [{"name": name} for name in ALLERGENS])


def downgrade() -> None:
    op.execute(allergen_table.delete().where(allergen_table.c.name.in_(ALLERGENS)))
