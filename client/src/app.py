from common.pyreact import useState, render, createElement as el
from common.jsutils import alert

def App():
    phrase, setPhrase = useState("")

    def handleSubmit():
        alert(f"Test phrase is : {phrase}")
        setPhrase("")

    def handleChange(event):
        target = event['target']
        setPhrase(target['value'])

    return el('div', None,
              el('label', {'htmlFor': 'testPhrase'}, "Test Phrase: "),
              el('input', {'id': 'testPhrase',
                           'onChange': handleChange,
                           'value': phrase
                          }
                ),
              el('button', {'onClick': handleSubmit}, "Submit"),
             )

render(App, None, 'root')

