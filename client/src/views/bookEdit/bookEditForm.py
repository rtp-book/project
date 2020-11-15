from common.pyreact import createElement as el, useContext
from common.pymui import TextField, RadioGroup, FormControlLabel, Radio, Button
from common.pymui import Paper, Divider, Typography
from main import UserCtx
from main.appTheme import Flexbox
from views.bookEdit.bookEditLookups import CategoriesList, PublishersList
from views.bookEdit.bookEditLookups import  FormatsList, ConditionsList


def BookEditForm(props):
    book = props['book']
    handleInputChange = props['handleInputChange']
    categories = props['categories']
    publishers = props['publishers']
    formats = props['formats']
    conditions = props['conditions']
    isDirty = props['isDirty']
    saveBook = props['saveBook']
    deleteBook = props['deleteBook']

    ctx = useContext(UserCtx)
    isLoggedIn = ctx['isLoggedIn']

    read_only = not isLoggedIn

    return el(Paper, {'style': {'padding': '0.5rem', 'marginTop': '0.8rem'}},
              el(Flexbox, None,
                 el(Flexbox, {'style': {'width': '40%',
                                        'flexDirection': 'column'}
                             },
                    el(TextField, {'label': "Title",
                                   'name': 'Title',
                                   'value': book.Title,
                                   'onChange': handleInputChange,
                                   'required': True,
                                   'autoFocus': True,
                                   'disabled': read_only
                                  }
                      ),
                    el(TextField, {'label': "Author",
                                   'name': 'Author',
                                   'value': book.Author or "",
                                   'onChange': handleInputChange,
                                   'disabled': read_only
                                  }
                      ),
                    el(TextField, {'select': True,
                                   'label': "Publisher",
                                   'name': 'Publisher',
                                   'value': book.Publisher or "",
                                   'onChange': handleInputChange,
                                   'SelectProps': {'native': True},
                                   'disabled': read_only
                                  },
                       el('option', {'value': ''}),
                       el(PublishersList, {'publishers': publishers}),
                      ),
                   ),
                 el(Divider, {'orientation': 'vertical', 'flexItem': True}),
                 el(Flexbox, {'flexWrap': 'wrap',
                              'style': {'width': '60%',
                                        'flexDirection': 'column'}
                             },
                    el(Flexbox, {'flexWrap': 'wrap'},
                       el(Flexbox, {'style': {'width': '70%'},
                                    'flexDirection': 'column'},
                          el(Flexbox, None,
                             el(TextField, {'select': True,
                                            'label': "Category",
                                            'name': 'Category',
                                            'value': book.Category or "",
                                            'onChange': handleInputChange,
                                            'SelectProps': {'native': True},
                                            'disabled': read_only
                                           },
                                el('option', {'value': ''}),
                                el(CategoriesList, {'categories': categories}),
                               ),

                            ),
                          el(Flexbox, None,
                             el(TextField, {'label': "Edition",
                                            'name': 'Edition',
                                            'value': book.Edition or "",
                                            'onChange': handleInputChange,
                                            'disabled': read_only
                                           }
                               ),
                             el(TextField, {'label': "DatePublished",
                                            'name': 'DatePublished',
                                            'value': book.DatePublished or "",
                                            'onChange': handleInputChange,
                                            'disabled': read_only
                                           }
                               ),
                            ),
                         ),
                       el(Flexbox, {'style': {'width': '30%'}},
                          el(RadioGroup, {'name': 'IsFiction',
                                          'style': {'margin': '0.7rem'},
                                          'value': book.IsFiction,
                                          'onChange': handleInputChange,
                                         },
                             el(FormControlLabel,
                                {'control': el(Radio, {'color': 'primary',
                                                       'size': 'small'}
                                              ),
                                 'value': 1,
                                 'label': 'Fiction',
                                 'disabled': read_only}
                               ),
                             el(FormControlLabel,
                                {'control': el(Radio, {'color': 'primary',
                                                       'size': 'small'}
                                              ),
                                 'value': 0,
                                 'label': 'Non-Fiction',
                                 'disabled': read_only}
                               ),
                            ),
                         ),
                      ),
                    el(Flexbox, {'flexWrap': 'wrap'},
                       el(TextField, {'select': True,
                                      'label': "Format",
                                      'name': 'Format',
                                      'style': {'width': '45%'},
                                      'value': book.Format or "",
                                      'onChange': handleInputChange,
                                      'SelectProps': {'native': True},
                                      'disabled': read_only
                                     },
                          el('option', {'value': ''}),
                          el(FormatsList, {'formats': formats}),
                         ),
                       el(TextField, {'label': "ISBN",
                                      'name': 'ISBN',
                                      'style': {'width': '36%'},
                                      'value': book.ISBN or "",
                                      'onChange': handleInputChange,
                                      'disabled': read_only
                                     }
                         ),
                       el(TextField, {'label': "Pages",
                                      'name': 'Pages',
                                      'style': {'width': '15%',
                                                'marginRight': 0},
                                      'value': book.Pages or "",
                                      'onChange': handleInputChange,
                                      'disabled': read_only
                                     }
                         ),
                      ),
                   ),
                ),
              el(Divider, None),
              el(Flexbox, None,
                 el(Flexbox, {'style': {'width': '30%',
                                        'flexDirection': 'column'}
                             },
                    el(TextField, {'label': "DateAcquired",
                                   'name': 'DateAcquired',
                                   'type': 'date',
                                   'style': {'marginBottom': '0.7rem'},
                                   'value': book.DateAcquired or "",
                                   'onChange': handleInputChange,
                                   'disabled': read_only
                                  }
                      ),
                    el(TextField, {'select': True,
                                   'label': "Condition",
                                   'name': 'Condition',
                                   'value': book.Condition or "",
                                   'onChange': handleInputChange,
                                   'SelectProps': {'native': True},
                                   'disabled': read_only
                                  },
                       el('option', {'value': ''}),
                       el(ConditionsList, {'conditions': conditions}),
                      ),
                    el(TextField, {'label': "Location",
                                   'name': 'Location',
                                   'style': {'marginTop': '0.7rem'},
                                   'value': book.Location or "",
                                   'onChange': handleInputChange,
                                   'disabled': read_only
                                  }
                      ),
                   ),
                 el(Divider, {'orientation': 'vertical', 'flexItem': True}),
                 el(Flexbox, {'style': {'width': '70%',
                                        'flexDirection': 'column'}
                             },
                    el(Flexbox, None,
                       el(TextField, {'label': "Notes",
                                      'name': 'Notes',
                                      'multiline': True,
                                      'rows': 4,
                                      'rowsMax': 4,
                                      'style': {'marginRight': 0},
                                      'value': book.Notes or "",
                                      'onChange': handleInputChange,
                                      'disabled': read_only
                                     }
                         ),
                      ),
                    el(Flexbox, {'justifyContent': 'flex-end',
                                 'style': {'marginTop': '0.7rem'}
                                },
                       el(Flexbox, {'justifyContent': 'center',
                                    'alignItems': 'center',
                                    'width': '100%'},
                          el(Typography, {'color': 'secondary'},
                             "A book title is required!"
                            ) if len(book.Title or "") == 0 else None
                         ),
                       el(Button, {'type': 'button',
                                   'color': 'secondary',
                                   'style': {'minWidth': '8rem'},
                                   'disabled': not isLoggedIn or
                                               book.ID == "NEW",
                                   'onClick': deleteBook
                                  }, "Delete"
                         ),
                       el(Button, {'type': 'button',
                                   'color': 'primary',
                                   'style': {'minWidth': '8rem',
                                             'marginLeft': '1rem'},
                                   'disabled': not (isLoggedIn and isDirty() and
                                                    len(book.Title or "") > 0),
                                   'onClick': saveBook
                                  }, "Save"
                         ),
                      ),
                   ),
                ),
             )

