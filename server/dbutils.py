from sqlalchemy import create_engine, inspect
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

import os
import logging

from dataModel import Base


DB_LOC = './database'
DB_NAME = 'books.db'
DB_FILE = os.path.join(DB_LOC, DB_NAME)

if __name__ == "__main__":
    fmt = "[%(asctime)s]|%(levelname)s|[%(module)s]:%(funcName)s()|%(message)s"
    logging.basicConfig(format=fmt, level=logging.ERROR)
log = logging.getLogger(__name__)


engine = create_engine(f'sqlite:///{DB_FILE}', echo=False, poolclass=NullPool)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    session.execute("PRAGMA foreign_keys = ON")
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def todict(model):
    return {col.key: getattr(model, col.key) for col in inspect(model).mapper.column_attrs}


def update_record(model: Base, record: dict) -> dict:
    record_id = record.pop('ID', None)

    if record_id:  # UPDATE
        try:
            with session_scope() as session:
                row = session.query(model).filter(model.ID == record_id)
                row.update(record)
                result = row.first()
                return {'success': todict(result) if result is not None else None}
        except Exception as e:
            log.error(e)
            return {'error': str(e)}
    else:  # INSERT
        try:
            with session_scope() as session:
                new_record = model(**record)
                session.add(new_record)
                session.flush()
                return {'success': todict(new_record)}
        except Exception as e:
            log.error(e)
            return {'error': str(e)}


def delete_record(model: Base, record: dict) -> dict:
    record_id = record.pop('ID', None)

    if record_id:
        try:
            with session_scope() as session:
                session.query(model).filter(model.ID == record_id).delete()
                return {'success': {}}
        except Exception as e:
            log.error(e)
            return {'error': str(e)}

    return {'success': None}


def create_db(autopopulate):
    if not os.path.exists(DB_LOC):
        os.mkdir(DB_LOC)

    Base.metadata.create_all(engine)

    if autopopulate:
        from testdata import populate_db
        populate_db(engine)


def connect(autopopulate=False):
    if not os.path.exists(DB_FILE):
        log.warning("Creating new DB")
        create_db(autopopulate)


def disconnect():
    engine.dispose()


def execute(stmt, params=()):
    try:
        with engine.connect() as conn:
            sql = text(stmt)
            conn.execute("PRAGMA foreign_keys = ON")
            trans = conn.begin()
            result = conn.execute(sql, params)
            rowcount = result.rowcount
            trans.commit()
            conn.close()
        return 'success', rowcount
    except Exception as e:
        log.error(e)
        if trans.is_active:
            trans.rollback()
        return 'error', str(e)


def select(stmt: str, params: dict):
    try:
        with engine.connect() as conn:
            sql = text(stmt)
            result = conn.execute(sql, params)
            cols = result.keys()
            rows = [dict(zip(cols, row)) for row in result]
            conn.close()
        return 'success', rows
    except Exception as e:
        log.error(e)
        return 'error', str(e)


def _main():
    sql = "SELECT name FROM sqlite_master WHERE type = :type"
    result, records = select(sql, dict(type='table'))
    print('Tables:', [tbl['name'] for tbl in records])


if __name__ == '__main__':
    connect(True)
    _main()
    disconnect()
