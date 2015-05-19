from datetime import datetime

from restler import decorators
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# Less common types
from sqlalchemy import Enum
# Currently unsupported types
from sqlalchemy import Interval, PickleType

# Standard/Generic Types
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Time,
    Float,
    Text,
    Binary
)

# More specific variants of the standard types
from sqlalchemy import (
    BigInteger,
    SmallInteger,
    Unicode,
    UnicodeText,
    LargeBinary,
    Numeric
)

# SQL Types
from sqlalchemy import (
    BIGINT,
    BINARY,
    BLOB,
    BOOLEAN,
    CHAR,
    CLOB,
    DATE,
    DATETIME,
    DECIMAL,
    FLOAT,
    INT,
    INTEGER,
    NCHAR,
    NVARCHAR,
    NUMERIC,
    REAL,
    SMALLINT,
    TEXT,
    TIME,
    TIMESTAMP,
    VARBINARY,
    VARCHAR
)

Base = declarative_base()

DATETIME_NOW = datetime.now()
TIME_NOW = DATETIME_NOW.time()
FLOAT_NUM = 1.01
A_STRING = "some string"
A_BINARY = '\xff\xd8\xff\xe1A\xecExif'


@decorators.sqlalchemy_serializer
class Model1(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    boolean = Column(Boolean, default=False)
    _date = Column(Date, default=DATETIME_NOW.date())
    _datetime = Column(DateTime, default=DATETIME_NOW)
    _float = Column(Float, default=FLOAT_NUM)
    string = Column(String(1000), default=A_STRING)
    text = Column(Text, default=A_STRING)
    _time = Column(Time, default=TIME_NOW)

    # unsupported types
    binary = Column(Binary, default=A_BINARY)
    interval = Column(Interval)
    large_binary = Column(LargeBinary, default=A_BINARY)
    pickle_type = Column(PickleType)


@decorators.sqlalchemy_serializer
class Poll(Base):
    __tablename__ = 'poll'

    id = Column(Integer, primary_key=True)
    question = Column(String(200))
    pub_date = Column(DateTime)
    choices = relationship('Choice', backref='poll')


@decorators.sqlalchemy_serializer
class Choice(Base):
    __tablename__ = 'choice'

    id = Column(Integer, primary_key=True)
    choice = Column(String(200))
    votes = Column(Integer)
    poll_id = Column(Integer, ForeignKey('poll.id'))
