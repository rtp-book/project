from common.pyreact import useState, useEffect, createElement as el, useContext
from common.pymui import Typography, AppBar, Toolbar, Tooltip, useSnackbar
from common.pymui import Container, Box, Paper, CircularProgress
from common.pymui import IconButton, CloseIcon, AddIcon
from common.urlutils import fetch, spaRedirect, buildParams
from main import UserCtx
from views.bookEdit.bookEditView import BookEdit
from views.bookList.bookListFilter import BooksFilterVu
from views.bookList.bookListTable import BooksTable


def BookList(props):
    params = props['params']

    book_id = params['id']

    books, setBooks = useState([])
    sortKey, setSortKey = useState('Title')
    showProgress, setShowProgress = useState(False)
    filterParams, setFilterParams = useState({})
    bookModal, setBookModal = useState(None)

    categories, setCategories = useState([])
    publishers, setPublishers = useState([])
    formats, setFormats = useState([])
    conditions, setConditions = useState([])

    ctx = useContext(UserCtx)
    isLoggedIn = ctx['isLoggedIn']

    snack = useSnackbar()

    def handleAdd():
        new_params = buildParams({'id': "NEW"})
        spaRedirect(f'/books{new_params}')

    def setEdit():
        if book_id:
            setBookModal(book_id)
        else:
            setBookModal(None)

    def sortBooks():
        book_list = [dict(tmp_book) for tmp_book in books]
        if len(book_list) > 0:
            setBooks(sorted(book_list, key=lambda k: k[sortKey] or ""))

    def on_fetch_error():
        snack.enqueueSnackbar("Error retrieving data!",
                              {'variant': 'error'}
                              )
        setShowProgress(False)

    def getBooks():
        isPending = True

        def _getBooks(data):
            book_list = data if data else []
            if isPending:
                if len(book_list) > 0:
                    setBooks(sorted(book_list, key=lambda k: k[sortKey]))
                else:
                    setBooks([])
                setShowProgress(False)

        def abort():
            nonlocal isPending
            isPending = False

        setShowProgress(True)
        fetch("/api/books", _getBooks,
              params=filterParams,
              onError=on_fetch_error
              )
        return abort

    def getLookup(table_name, setState):
        isPending = True

        def _getLookup(data):
            if isPending:
                if data:
                    setState(data)
                else:
                    setState([])

        def abort():
            nonlocal isPending
            isPending = False

        fetch(f"/api/lookup/{table_name}", _getLookup)
        return abort

    def getLookups():
        getLookup('Categories', setCategories)
        getLookup('Publishers', setPublishers)
        getLookup('Formats', setFormats)
        getLookup('Conditions', setConditions)

    useEffect(getBooks, [filterParams])
    useEffect(sortBooks, [sortKey])
    useEffect(setEdit, [book_id])
    useEffect(getLookups, [])

    return el(Container, None,
              el(AppBar, {'position': 'static',
                          'style': {'marginBottom': '0.5rem'}
                         },
                 el(Toolbar, {'variant': 'dense'},
                    el(Tooltip, {'title': 'Add new book'},
                       el(IconButton, {'edge': 'start',
                                       'color': 'inherit',
                                       'padding': 'none',
                                       'onClick': handleAdd
                                      }, el(AddIcon, None)
                         )
                      ) if isLoggedIn else None,
                    el(Box, {'width': '100%'},
                       el(Typography, {'variant': 'h6'}, "Books")
                      ),
                    el(IconButton, {'edge': 'end',
                                    'color': 'inherit',
                                    'onClick': lambda: spaRedirect('/')
                                   }, el(CloseIcon, None)
                      ),
                   ),
                ),
              el(BooksFilterVu, {'categories': categories,
                                 'setFilterParams': setFilterParams}
                ),
              el(Paper, {'style': {'padding': '0.5rem', 'marginTop': '0.8rem'}},
                 el(BooksTable, {'books': books, 'setSortKey': setSortKey})
                ),
              el(BookEdit, {'bookId': bookModal,
                            'categories': categories,
                            'publishers': publishers,
                            'formats': formats,
                            'conditions': conditions,
                            'getBooks': getBooks
                           }),
              el(CircularProgress,
                 {'style': {'position': 'absolute',
                            'top': '30%',
                            'left': '50%',
                            'marginLeft': -12}
                 }) if showProgress else None
             )

