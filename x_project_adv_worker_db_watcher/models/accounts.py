__all__ = ['Accounts', 'MVAccounts']
from sqlalchemy import (Column, BigInteger, Boolean, Integer, select, Index)
from sqlalchemy_utils import ChoiceType

from x_project_adv_worker_db_watcher.choiceTypes import ProjectType
from .__libs__.sql_view import create_view
from .meta import Base


class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column(BigInteger, primary_key=True)
    blocked = Column(Boolean, default=False)
    project = Column(ChoiceType(ProjectType, impl=Integer()))

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVAccounts(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_accounts',
        select([
            Accounts.id,
            Accounts.blocked,
            Accounts.project,
        ]).select_from(Accounts),
        is_mat=True)


Index('ix_mv_accounts_id', MVAccounts.id, unique=True)
