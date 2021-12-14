from common.pyreact import useState, react_component, Fragment, Input
from common.pymui import Box, AddIcon, IconButton
from common.pymui import TableContainer, Table
from common.pymui import TableHead, TableBody, TableRow, TableCell


@react_component
def ItemEditCell(props):
    field = props['field']
    setEditValues = props['setEditValues']
    editValues = props['editValues']
    checkSaveItem = props['checkSaveItem']

    field_value = editValues[field]

    def handleChange(event):
        event.preventDefault()
        target = event['target']
        value = target['value']
        key = target['id']

        new_editValues = dict(editValues)
        new_editValues.update({key: value})
        setEditValues(new_editValues)

    def handleKeyPress(event):
        key = event['key']
        if key == 'Enter':
            checkSaveItem()

    return TableCell(None,
                     Input({'id': field,
                            'onKeyPress': handleKeyPress,
                            'onChange': handleChange,
                            'value': field_value,
                            'style': {'width': '10rem', 'margin': '-4px'}}
                           )
                     )


@react_component
def ItemCell(props):
    value = props['value']

    return TableCell(None,
                     Box({'width': '10rem', 'whiteSpace': 'nowrap'}, value)
                     )


@react_component
def ItemRowVu(props):
    item = props['item']
    fields = props['fields']
    selected = props['selected']
    setSelected = props['setSelected']
    editValues = props['editValues']
    setEditValues = props['setEditValues']
    checkSaveItem = props['checkSaveItem']

    def handleClick():
        if selected:
            checkSaveItem()

    def handleDoubleClick():
        setEditValues(dict(item))
        setSelected(item['ID'])

    if item['ID'] == selected:
        return TableRow(None,
                        [ItemEditCell({'key': field,
                                       'field': field,
                                       'setEditValues': setEditValues,
                                       'editValues': editValues,
                                       'checkSaveItem': checkSaveItem,
                                       }) for field in fields]
                        )
    else:
        return TableRow({'onClick': handleClick,
                         'onDoubleClick': handleDoubleClick},
                        [ItemCell({'key': field,
                                   'value': item[field],
                                   }) for field in fields]
                        )


@react_component
def ItemRows(props):
    items = props['items']
    fields = props['fields']
    setItems = props['setItems']
    saveItem = props['saveItem']

    selected, setSelected = useState(None)
    editValues, setEditValues = useState({})

    def checkSaveItem():
        old_item = next((item for item in items if item['ID'] == selected), {})
        new_item = dict(editValues)
        if new_item['ID'] == "NEW":
            new_item.pop("ID")
        # Transcrypt differs from CPython on object equality so check each value
        if len(new_item) != len(old_item) or \
                len([key for key, val in new_item.items()
                     if val != old_item[key]]) > 0:
            saveItem(new_item)
        setEditValues({})
        setSelected(None)

    def handleAdd():
        new_items = [dict(item) for item in items]
        new_item = {field: "" for field in fields}
        new_item['ID'] = "NEW"
        new_items.append(new_item)
        setItems(new_items)
        setEditValues(new_item)
        setSelected("NEW")

    def itemToRow(item):
        return ItemRowVu({'key': item['ID'],
                          'item': item,
                          'fields': fields,
                          'selected': selected,
                          'setSelected': setSelected,
                          'editValues': editValues,
                          'setEditValues': setEditValues,
                          'checkSaveItem': checkSaveItem,
                          }
                         )

    @react_component
    def AddItem():
        if selected == "NEW":
            return None
        else:
            return TableRow({'key': 'ADD'},
                            TableCell({'variant': 'footer',
                                       'align': 'center',
                                       'colSpan': len(fields)},
                                      IconButton({'edge': 'end',
                                                  'color': 'primary',
                                                  'size': 'small',
                                                  'padding': 'none',
                                                  'onClick': handleAdd
                                                  }, AddIcon(None)
                                                 )
                                      )
                            )

    if len(items) > 0:
        return Fragment(None,
                        [itemToRow(item) for item in items if item],
                        AddItem(None)
                        )
    else:
        return AddItem(None)


@react_component
def ItemsList(props):
    items = props['items']
    fields = props['fields']
    saveItem = props['saveItem']
    setItems = props['setItems']

    @react_component
    def HeaderCols():
        return TableRow(None,
                        [TableCell({'key': field, 'fields': fields}, field)
                         for field in fields]
                        )

    return TableContainer({'style': {'maxHeight': '10.5rem'}},
                          Table({'size': 'small', 'stickyHeader': True},
                                TableHead(None,
                                          HeaderCols(None),
                                          ),
                                TableBody(None,
                                          ItemRows({'items': items,
                                                    'fields': fields,
                                                    'setItems': setItems,
                                                    'saveItem': saveItem}),
                                          )
                                )
                          )
