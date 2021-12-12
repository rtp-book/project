from common.pyreact import react_component
from common.urlutils import buildParams, spaRedirect
from common.pymui import Box, Link, Tooltip
from common.pymui import TableContainer, Table
from common.pymui import TableHead, TableBody, TableRow, TableCell


@react_component
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

    return TableRow({'onClick': handleEdit},
                    TableCell(None,
                              Tooltip({'title': title if title else ''},
                                      Box({'width': '10rem',
                                           'textOverflow': 'ellipsis',
                                           'overflow': 'hidden',
                                           'whiteSpace': 'nowrap'}, title),
                                      )
                              ),
                    TableCell(None,
                              Box({'width': '6rem', 'whiteSpace': 'nowrap'}, author)),
                    TableCell(None,
                              Box({'width': '5rem'}, book_type)),
                    TableCell(None,
                              Box({'width': '8rem'}, category)),
                    TableCell(None,
                              Box({'width': '6rem'}, book_fmt)),
                    TableCell(None,
                              Box({'width': '5rem'}, location)),
                    )


@react_component
def BooksTable(props):
    books = props['books']
    setSortKey = props['setSortKey']

    def bookToRow(book):
        return BookRowVu({'key': book['ID'], 'book': book})

    @react_component
    def BookRows():
        if len(books) > 0:
            return [bookToRow(book) for book in books if book]
        else:
            return TableRow({'key': '0'})

    @react_component
    def HeaderSort(props_):
        field = props_['field']

        def handleSort(event):
            event.preventDefault()
            setSortKey(field)

        return TableCell(None,
                         Link({'href': '#', 'onClick': handleSort}, field)
                         )

    return TableContainer({'style': {'maxHeight': '30rem'}},
                          Table(None,
                                TableHead(None,
                                          TableRow(None,
                                                   HeaderSort({'field': 'Title'}),
                                                   HeaderSort({'field': 'Author'}),
                                                   HeaderSort({'field': 'Genre'}),
                                                   HeaderSort({'field': 'Category'}),
                                                   HeaderSort({'field': 'Format'}),
                                                   HeaderSort({'field': 'Location'}),
                                                   ),
                                          ),
                                TableBody(None,
                                          BookRows(None)
                                          )
                                )
                          )
