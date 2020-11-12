import sqlite3
import os
import logging


DB_LOC = './database'
DB_NAME = 'books.db'
DB_FILE = os.path.join(DB_LOC, DB_NAME)

if __name__ == "__main__":
    fmt = "[%(asctime)s]|%(levelname)s|[%(module)s]:%(funcName)s()|%(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)
log = logging.getLogger(__name__)


def create_db(autopopulate):
    if not os.path.exists(DB_LOC):
        os.mkdir(DB_LOC)

    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()

        # sqlite foreign key support is off by default
        cur.execute("PRAGMA foreign_keys = ON")
        conn.commit()

        # Create tables
        cur.execute("CREATE TABLE Categories ("
                    "ID INTEGER PRIMARY KEY NOT NULL, "
                    "Category TEXT UNIQUE)")
        cur.execute("CREATE TABLE Publishers ("
                    "ID INTEGER PRIMARY KEY NOT NULL, "
                    "Publisher TEXT UNIQUE)")
        cur.execute("CREATE TABLE Conditions ("
                    "ID INTEGER PRIMARY KEY NOT NULL, "
                    "Code TEXT UNIQUE, "
                    "Condition TEXT)")
        cur.execute("CREATE TABLE Formats ("
                    "ID INTEGER PRIMARY KEY NOT NULL, "
                    "Format TEXT UNIQUE)")
        cur.execute("CREATE TABLE Users ("
                    "ID INTEGER PRIMARY KEY NOT NULL, "
                    "Username TEXT UNIQUE, "
                    "Password TEXT)")
        conn.commit()

        cur.execute("CREATE TABLE Books ("
                    "ID INTEGER PRIMARY KEY NOT NULL,"
                    "Title TEXT NOT NULL,"
                    "Author TEXT,"
                    "Publisher TEXT "
                      "REFERENCES Publishers(Publisher) "
                      "ON UPDATE CASCADE ON DELETE RESTRICT,"
                    "IsFiction BOOLEAN DEFAULT 0,"
                    "Category TEXT "
                      "REFERENCES Categories(Category) "
                      "ON UPDATE CASCADE ON DELETE RESTRICT,"
                    "Edition TEXT,"
                    "DatePublished TEXT,"
                    "ISBN TEXT,"
                    "Pages INTEGER,"
                    "DateAcquired DATE,"
                    "Condition TEXT "
                      "REFERENCES Conditions(Code) "
                      "ON UPDATE CASCADE ON DELETE RESTRICT,"
                    "Format TEXT "
                      "REFERENCES Formats(Format) "
                      "ON UPDATE CASCADE ON DELETE RESTRICT,"
                    "Location TEXT,"
                    "Notes TEXT"
                    ")"
                   )
        conn.commit()
        cur.close()

        if autopopulate:
            from testdata import populate_db
            populate_db(conn)


def connect(autopopulate=False):
    if not os.path.exists(DB_FILE):
        log.warning("Creating new DB")
        create_db(autopopulate)


def execute(stmt, params=()):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            curs = conn.cursor()
            curs.execute(stmt, params)
            rowcount = curs.rowcount
            curs.close()
            conn.commit()
        return 'success', rowcount
    except Exception as e:
        log.error(e)
        return 'error', str(e)


def select(stmt, params=()):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            curs = conn.cursor()
            curs.execute(stmt, params)
            desc = curs.description
            cols = [fld[0] for fld in desc]
            rowset = curs.fetchall()
            rows = [dict(zip(cols, row)) for row in rowset]
            curs.close()
        return 'success', rows
    except Exception as e:
        log.error(e)
        return 'error', str(e)


def _main():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        sql = "SELECT name FROM sqlite_master WHERE type = ?"
        cur.execute(sql, ('table',))
        data = cur.fetchall()
        print('Tables:', [tbl[0] for tbl in data])


if __name__ == '__main__':
    connect(True)
    _main()

