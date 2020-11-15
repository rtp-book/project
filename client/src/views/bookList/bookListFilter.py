from common.pyreact import useState, createElement as el
from common.pymui import TextField, Button, Paper
from main.appTheme import Flexbox
from views.bookEdit.bookEditLookups import CategoriesList



def BooksFilterVu(props):
    categories = props['categories']
    setFilterParams = props['setFilterParams']

    Title, setTitle = useState("")
    Author, setAuthor = useState("")
    IsFiction, setIsFiction = useState("")
    Category, setCategory = useState("")
    ISBN, setISBN = useState("")

    def setState(field, value):
        switch = dict(Title=setTitle,
                      Author=setAuthor,
                      IsFiction=setIsFiction,
                      Category=setCategory,
                      ISBN=setISBN
                     )
        switch[field](value)

    def handleInputChange(event):
        event.preventDefault()
        target = event['target']
        value = target['value']
        key = target['name']
        setState(key, value)

    def handleFilter():
        params = dict(Title=Title,
                      Author=Author,
                      IsFiction=IsFiction,
                      Category=Category,
                      ISBN=ISBN
                     )
        filters = {key: val for key, val in params.items() if len(val) > 0}
        setFilterParams(filters)

    filter_width = '17%'

    return el(Paper, None,
              el(Flexbox, {'flexWrap': 'wrap', 'style': {'margin': '0.5rem'}},
                 el(TextField, {'label': "Title",
                                'name': 'Title',
                                'style': {'width': filter_width},
                                'value': Title,
                                'onChange': handleInputChange,
                               }
                   ),
                 el(TextField, {'label': "Author",
                                'name': 'Author',
                                'style': {'width': filter_width},
                                'value': Author,
                                'onChange': handleInputChange,
                               }
                   ),
                 el(TextField, {'label': "Genre",
                                'name': 'IsFiction',
                                'style': {'width': filter_width},
                                'value': IsFiction,
                                'onChange': handleInputChange,
                                'select': True,
                                'SelectProps': {'native': True},
                               },
                    el('option', {'value': ''}, ""),
                    el('option', {'value': '1'}, "Fiction"),
                    el('option', {'value': '0'}, "Non-Fiction"),
                   ),
                 el(TextField, {'label': "Category",
                                'name': 'Category',
                                'style': {'width': filter_width},
                                'value': Category,
                                'onChange': handleInputChange,
                                'select': True,
                                'SelectProps': {'native': True},
                               },
                    el('option', {'value': ''}),
                    el(CategoriesList, {'categories': categories}),
                   ),
                 el(TextField, {'label': "ISBN",
                                'name': 'ISBN',
                                'style': {'width': filter_width},
                                'value': ISBN,
                                'onChange': handleInputChange,
                               }
                   ),
                 el(Button, {'type': 'button',
                             'color': 'primary',
                             'size': 'small',
                             'style': {'minWidth': '7rem', 'margin': '0.5rem'},
                             'onClick': handleFilter
                            }, "Filter"
                   ),
                )
             )

