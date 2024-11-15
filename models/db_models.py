import enum
from datetime import date

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class RoleUserEnum(str, enum.Enum):
    ADMIN = 'admin'
    USER = 'user'


class TypeQuestionEnum(str, enum.Enum):
    ANSWER_TEXT = 'Ответ текстом'
    ANSWER_CHOICE_ONE = 'Ответ выбором 1 варианта'
    ANSWER_CHOICE_MANY = 'Ответ выбором n вариантов'


class User(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    username: Mapped[str] = mapped_column(
        unique=True, index=True
    )
    email: Mapped[str] = mapped_column(
        unique=True, index=True
    )
    password: Mapped[str] = mapped_column(
        nullable=False
    )
    role: Mapped[str] = mapped_column(
        nullable=False, default=RoleUserEnum.USER,
    )
    polls = relationship(
        'Poll', back_populates='admin', cascade='all, delete, delete-orphan'
    )

    # Связи
    user_results = relationship('UserResult', back_populates='user')



class Poll(Base):

    __tablename__ = 'polls'

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    title: Mapped[str] = mapped_column(
        unique=True, index=True, nullable=False
    )
    date_start: Mapped[date] = mapped_column(
        nullable=False
    )
    date_end: Mapped[date] = mapped_column(
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )

    # Связи
    user = relationship('User', back_populates='polls')
    questions = relationship('Question', back_populates='poll', cascade='all, delete, delete-orphan')
    user_results = relationship('UserResult', back_populates='poll')


class Question(Base):

    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    title: Mapped[str] = mapped_column(
        unique=True, nullable=False, index=True
    )
    answer: Mapped[TypeQuestionEnum] = mapped_column(
        Enum(TypeQuestionEnum),
        default=TypeQuestionEnum.ANSWER_CHOICE_ONE
    )
    poll_id: Mapped[int] = mapped_column(
        ForeignKey('polls.id'), nullable=False
    )

    # Связи
    poll = relationship('Poll', back_populates='questions')


class UserResult(Base):

    __tablename__ = 'user_results'

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )
    poll_id: Mapped[int] = mapped_column(
        ForeignKey('polls.id'), nullable=False
    )

    # Связи
    user = relationship('User', back_populates='user_results')
    poll = relationship('Poll', back_populates='user_results')