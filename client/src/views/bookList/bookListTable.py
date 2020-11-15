from common.pyreact import createElement as el
from common.urlutils import buildParams, spaRedirect
from common.pymui import Box, Link, Tooltip
from common.pymui import TableContainer, Table
from common.pymui import TableHead, TableBody, TableRow, TableCell


def BookRowVu(props):
    book = props['book']

    book_id = book['ID']
    title = book['Title']
    author = book['Author']
    book_type = "Fiction" if book['IsFiction'] else "Non-Fiction"
    category = book['Category']
    book_fmt = book['Format']
    location = book['Location']

    def handleEdit():
        params = buildParams({'id': book_id})
        spaRedirect(f'/books{params}')

    return el(TableRow, {'onClick': handleEdit},
              el(TableCell, None,
                 el(Tooltip, {'title': title if title else ''},
                    el(Box, {'width': '10rem',
                             'textOverflow': 'ellipsis',
                             'overflow': 'hidden',
                             'whiteSpace': 'nowrap'}, title),
                   )
                ),
              el(TableCell, None,
                 el(Box, {'width': '6rem', 'whiteSpace': 'nowrap'}, author)),
              el(TableCell, None,
                 el(Box, {'width': '5rem'}, book_type)),
              el(TableCell, None,
                 el(Box, {'width': '8rem'}, category)),
              el(TableCell, None,
                 el(Box, {'width': '6rem'}, book_fmt)),
              el(TableCell, None,
                 el(Box, {'width': '5rem'}, location)),
             )


def BooksTable(props):
    books = props['books']
    setSortKey = props['setSortKey']

    def bookToRow(book):
        return el(BookRowVu, {'key': book['ID'], 'book': book})

    def BookRows():
        if len(books) > 0:
            return [bookToRow(book) for book in books if book]
        else:
            return el(TableRow, {'key': '0'})

    def HeaderSort(props_):
        field = props_['field']

        def handleSort(event):
            event.preventDefault()
            setSortKey(field)

        return el(TableCell, None,
                  el(Link, {'href': '#', 'onClick': handleSort}, field)
                 )

    return el(TableContainer, {'style': {'maxHeight': '30rem'}},
              el(Table, None,
                 el(TableHead, None,
                    el(TableRow, None,
                       el(HeaderSort, {'field': 'Title'}),
                       el(HeaderSort, {'field': 'Author'}),
                       el(HeaderSort, {'field': 'Genre'}),
                       el(HeaderSort, {'field': 'Category'}),
                       el(HeaderSort, {'field': 'Format'}),
                       el(HeaderSort, {'field': 'Location'}),
                      ),
                   ),
                 el(TableBody, None,
                    el(BookRows, None)
                   )
                )
             )

