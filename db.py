from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 'mysql://poststatview-database.cexll1c2pdsq.ap-northeast-2.rds.amazonaws.com:3306/'
db_host = 'poststatview-database.cexll1c2pdsq.ap-northeast-2.rds.amazonaws.com'
scheme = 'mfr'

SQLALCHEMY_DATABASE_URL = "mysql://%s:%s@%s:%s/%s" % (
    username,
    password,
    db_host,
    3306,
    scheme
)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()