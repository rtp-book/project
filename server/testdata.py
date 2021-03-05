from datetime import date
from sqlalchemy.orm import Session

from dataModel import Categories, Publishers, Conditions, Formats, Users, Books


def populate_db(engine):
    categories = ['Computers & Tech',
                  'Biographies',
                  'Sci-Fi & Fantasy',
                  'Arts & Music',
                  'History']

    publishers = ['No Starch Press', 'Del Rey Books']

    conditions = {'F': 'Fine/Like New',
                  'NF': 'Near Fine',
                  'VG': 'Very Good',
                  'G': 'Good',
                  'FR': 'Fair',
                  'P': 'Poor'}

    formats = ['Hardcover', 'Paperback', 'Oversized', 'Pamphlet', 'E-book']

    books = [
        dict(Title='React to Python',
             Author='Sheehan',
             IsFiction=0,
             Category='Computers & Tech',
             DateAcquired=date(2020, 12, 1),
             Condition='F',
             Location='A3'),
        dict(Title='I Robot',
             Author='Isaac Asimov',
             Publisher='Del Rey Books',
             ISBN='055338256X',
             IsFiction=1,
             Category='Sci-Fi & Fantasy',
             Format='Paperback'),
        dict(Title='The C Programming Language',
             Author='Kernighan & Ritchie',
             ISBN='0131103628',
             IsFiction=0,
             Category='Computers & Tech'),
    ]

    session = Session(bind=engine)
    session.execute("PRAGMA foreign_keys = ON")
    session.add_all([Categories(Category=category) for category in categories])
    session.add_all([Publishers(Publisher=publisher) for publisher in publishers])
    session.add_all([Conditions(Code=key, Condition=val) for key, val in conditions.items()])
    session.add_all([Formats(Format=fmt) for fmt in formats])
    session.add(Users(Username='admin', Password=''))
    session.commit()
    session.add_all([Books(**book) for book in books])
    session.commit()
    session.close()
