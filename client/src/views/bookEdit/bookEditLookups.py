from common.pyreact import react_component, Option


@react_component
def CategoriesList(props):
    categories = props['categories']

    def categoryToRow(author):
        category_id = author['ID']
        category_name = author['Category']

        return Option({'key': category_id,
                       'value': category_name}, category_name)

    return [categoryToRow(category) for category in categories]


@react_component
def PublishersList(props):
    publishers = props['publishers']

    def publisherToRow(publisher):
        publisher_id = publisher['ID']
        publisher_name = publisher['Publisher']

        return Option({'key': publisher_id,
                       'value': publisher_name}, publisher_name)

    return [publisherToRow(publisher) for publisher in publishers]


@react_component
def ConditionsList(props):
    conditions = props['conditions']

    def conditionToRow(condition):
        condition_id = condition['ID']
        condition_code = condition['Code']
        condition_name = condition['Condition']

        return Option({'key': condition_id,
                       'value': condition_code}, condition_name)

    return [conditionToRow(condition) for condition in conditions]


@react_component
def FormatsList(props):
    formats = props['formats']

    def formatToRow(publisher):
        format_id = publisher['ID']
        format_name = publisher['Format']

        return Option({'key': format_id,
                       'value': format_name}, format_name)

    return [formatToRow(format_) for format_ in formats]
