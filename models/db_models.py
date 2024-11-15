import enum
from datetime import date

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TypeQuestionEnum(str, enum.Enum):
    ANSWER_TEXT = 'Ответ текстом'
    ANSWER_CHOICE_ONE = 'Ответ выбором 1 варианта'
    ANSWER_CHOICE_MANY = 'Ответ выбором n вариантов'


class User(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False)

    polls = relationship('Poll', back_populates='admin', cascade='all, delete, delete-orphan')



class Poll(Base):

    __tablename__ = 'polls'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    date_start: Mapped[date] = mapped_column(nullable=False)
    date_end: Mapped[date] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='polls')
    questions = relationship('Question', back_populates='poll', cascade='all, delete, delete-orphan')


class Question(Base):

    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    answer: Mapped[TypeQuestionEnum] = mapped_column(Enum(TypeQuestionEnum), default=TypeQuestionEnum.ANSWER_CHOICE_ONE)
    poll_id: Mapped[int] = mapped_column(ForeignKey('polls.id'), nullable=False)

    poll = relationship('Poll', back_populates='questions')