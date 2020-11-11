import sqlalchemy as sa
from magnet.database import Base


class Dummy(Base):
    __tablename__ = "dummy"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)

    __table_args__ = (
        {'comment': '検証用に使うテーブル。本番環境では、本テーブルにデータが存在することはありません。'}
    )
