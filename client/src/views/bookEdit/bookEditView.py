from common.jsutils import confirm
from common.pyreact import useState, useEffect, createElement as el, Modal
from common.pymui import Typography, AppBar, Toolbar, Box, useSnackbar
from common.pymui import IconButton, CloseIcon
from common.urlutils import fetch, spaRedirect
from main.appTheme import modalStyles
from views.bookEdit.bookEditForm import BookEditForm


book_template = dict(
    ID=None,
    Title="",
    Author=None,
    Publisher=None,
    IsFiction=0,
    Category=None,
    Edition=None,
    DatePublished=None,
    ISBN=None,
    Pages=None,
    DateAcquired=None,
    Condition=None,
    Format=None,
    Location=None,
    Notes=None
)


def BookEdit(props):
    bookId = props['bookId']
    categories = props['categories']
    publishers = props['publishers']
    formats = props['formats']
    conditions = props['conditions']
    getBooks = props['getBooks']

    book, setBook = useState(book_template)
    bookInitial, setBookInitial = useState(book_template)
    modalState = bool(bookId)

    snack = useSnackbar()

    def handleInputChange(event):
        event.preventDefault()
        target = event['target']
        value = target['value']
        key = target['name']

        if key == "IsFiction":  # RadioGroup sends str instead of int
            value = int(value)

        tmp_book = dict(book)
        tmp_book.update({key: value})
        setBook(tmp_book)

    def isDirty():
        changed = [key for key, val in book.items() if val != bookInitial[key]]
        return len(changed) > 0

    def saveBook():
        tmp_book = dict(book)
        if tmp_book['ID'] == "NEW":
            tmp_book.pop('ID')

        fetch(f"/api/book", on_update_success,
              method='POST', data=tmp_book, onError=on_update_error)

    def deleteBook():
        if confirm(f"Are you sure you want to delete {book.Title}?"):
            fetch(f"/api/book", on_update_success,
                  method='DELETE', data=book, onError=on_update_error)

    def on_update_success():
        getBooks()
        snack.enqueueSnackbar("Book was updated!", {'variant': 'success'})
        spaRedirect('/books')

    def on_update_error():
        snack.enqueueSnackbar("Error updating data!", {'variant': 'error'})

    def on_fetch_error():
        snack.enqueueSnackbar("Error retrieving data!", {'variant': 'error'})

    def getBook():
        def _getBook(data):
            if data:
                tmp_book = dict(book)
                tmp_book.update(**data)
                setBookInitial(tmp_book)
            else:
                setBookInitial(book_template)

        if bookId == "NEW":
            new_book = dict(book_template)
            new_book.update(ID=bookId)
            setBookInitial(new_book)
        elif bookId:
            fetch(f"/api/book", _getBook,
                  params={'id': bookId},
                  onError=on_fetch_error
                 )

    def update_book():
        tmp_book = dict(bookInitial)
        setBook(tmp_book)

    useEffect(getBook, [bookId])
    useEffect(update_book, [bookInitial])

    return el(Modal, {'isOpen': modalState,
                      'style': modalStyles,
                      'ariaHideApp': False,
                     },
              el(AppBar, {'position': 'static',
                          'style': {'marginBottom': '0.5rem'}
                         },
                 el(Toolbar, {'variant': 'dense'},
                    el(Box, {'width': '100%'},
                       el(Typography, {'variant': 'h6'}, book.Title)
                      ),
                    el(IconButton, {'edge': 'end',
                                    'color': 'inherit',
                                    'onClick': lambda: spaRedirect('/books')
                                   }, el(CloseIcon, None)
                      ),
                   ),
                ),
              el(BookEditForm, {'book': book,
                                'handleInputChange': handleInputChange,
                                'categories': categories,
                                'publishers': publishers,
                                'formats': formats,
                                'conditions': conditions,
                                'isDirty': isDirty,
                                'saveBook': saveBook,
                                'deleteBook': deleteBook
                               }),
             )

