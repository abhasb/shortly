"""rename_short_url_to_short_code_add_expiration_time

Revision ID: 0e5a47bc5233
Revises: 
Create Date: 2026-02-26 15:19:25.506042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e5a47bc5233'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Rename primary key column short_url -> short_code
    op.alter_column("urls", "short_url", new_column_name="short_code")

    # Rename the index that referenced the old column name
    op.drop_index("ix_urls_short_url", table_name="urls")
    op.create_index("ix_urls_short_code", "urls", ["short_code"])

    # Add the missing expiration_time column
    op.add_column("urls", sa.Column("expiration_time", sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("urls", "expiration_time")

    op.drop_index("ix_urls_short_code", table_name="urls")
    op.create_index("ix_urls_short_url", "urls", ["short_url"])

    op.alter_column("urls", "short_code", new_column_name="short_url")
