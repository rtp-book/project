from common.pyreact import createElement as el


def CategoriesList(props):
    categories = props['categories']

    def categoryToRow(author):
        category_id = author['ID']
        category_name = author['Category']

        return el('option', {'key': category_id,
                             'value': category_name}, category_name)

    return [categoryToRow(category) for category in categories]


def PublishersList(props):
    publishers = props['publishers']

    def publisherToRow(publisher):
        publisher_id = publisher['ID']
        publisher_name = publisher['Publisher']

        return el('option', {'key': publisher_id,
                             'value': publisher_name}, publisher_name)

    return [publisherToRow(publisher) for publisher in publishers]


def ConditionsList(props):
    conditions = props['conditions']

    def conditionToRow(condition):
        condition_id = condition['ID']
        condition_code = condition['Code']
        condition_name = condition['Condition']

        return el('option', {'key': condition_id,
                             'value': condition_code}, condition_name)

    return [conditionToRow(condition) for condition in conditions]


def FormatsList(props):
    formats = props['formats']

    def formatToRow(publisher):
        format_id = publisher['ID']
        format_name = publisher['Format']

        return el('option', {'key': format_id,
                             'value': format_name}, format_name)

    return [formatToRow(format_) for format_ in formats]

