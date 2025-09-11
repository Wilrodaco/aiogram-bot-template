"""Add unique constraint to users.user_id"""

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("uq_users_user_id", "users", ["user_id"])


def downgrade() -> None:
    op.drop_constraint("uq_users_user_id", "users", type_="unique")
