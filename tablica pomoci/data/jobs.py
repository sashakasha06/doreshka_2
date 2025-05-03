from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase
from datetime import datetime

class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_leader = Column(Integer, ForeignKey('users.id'))
    job = Column(String, nullable=True)
    work_size = Column(Integer, nullable=True)
    collaborators = Column(String, nullable=True)
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime, nullable=True)
    is_finished = Column(Boolean, default=False)

    user = relationship('User')