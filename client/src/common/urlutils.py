import time
from common.pyreact import ReactGA, createElement as el
from common.pymui import Link as MuiLink
from common.jsutils import console

# __pragma__ ('skip')
from common import require, window, JSON, __new__
# __pragma__ ('noskip')


polyfill = require("@babel/polyfill")  # required by async/await


# __pragma__ ('kwargs')
async def fetch(url, callback=None, **kwargs):
    ReactGA.event({'category': 'api', 'action': 'request', 'label': url})
    t_start = time.time()
    on_error = kwargs.pop('onError', None)
    redirect = kwargs.pop('redirect', True)
    method = kwargs.pop('method', 'GET')
    try:
        if method == 'POST' or method == 'DELETE':
            data = kwargs.pop('data', None)
            # headers needs to be a plain JS object
            headers = {'Content-Type': 'application/json;'}  # __:jsiter
            response = await window.fetch(url, {'method': method,
                                                'headers': headers,
                                                'body': JSON.stringify(data)
                                               }
                                          )
        else:
            kw_params = kwargs.pop('params', {})
            params = buildParams(kw_params)
            response = await window.fetch(f"{url}{params}")

        if response.status == 401:
            console.error("401 - Session Expired")
            if redirect:
                redirToLoginPage()
            raise Exception("Unauthorized")
        elif response.status != 200:
            console.error('Fetch error - Status Code: ' + response.status)
            if on_error:
                on_error()
        else:
            json_data = await response.json()
            t_elapsed = time.time() - t_start
            ReactGA.timing({'category': 'API',
                            'variable': 'fetch',
                            'value': int(t_elapsed * 1000),
                            'label': url}
                           )

            error = dict(json_data).get('error', None)
            if error:
                raise Exception(error)
            else:
                result = dict(json_data).get('success', None)
                if callback:
                    callback(result)
    except object as e:
        console.error(str(e))
        if on_error:
            on_error()

# __pragma__ ('nokwargs')


def buildParams(param_dict: dict):
    param_list = [f"&{key}={window.encodeURIComponent(val)}" 
                  for key, val in param_dict.items() if val]
    params = ''.join(param_list)
    return f"?{params[1:]}" if len(params) > 0 else ''


def spaRedirect(url):
    window.history.pushState(None, '', url)
    window.dispatchEvent(__new__(window.PopStateEvent('popstate')))


def redirToLoginPage():
    # Check if redir is already in params
    params = __new__(window.URLSearchParams(window.location.search)).entries()
    param_dict = {p[0]: p[1] for p in params if p}
    redir = param_dict.get('redir', None)

    if redir:
        hrefNew = f"/?login=show&redir={window.encodeURIComponent(redir)}"
    else:
        hrefCurrent = window.location.href
        if hrefCurrent:
            encoded_href = window.encodeURIComponent(hrefCurrent)
            hrefNew = f"/?login=show&redir={encoded_href}"
        else:
            hrefNew = '/?login=show'

    window.location.href = hrefNew


def Link(props):
    """Internal SPA link with browser history"""

    def onClick(event):
        event.preventDefault()
        spaRedirect(props['to'])

    def onClickAlt(event):
        event.preventDefault()
        props['onClick']()

    if props['onClick']:
        return el(MuiLink, {'href': props['to'],
                            'onClick': onClickAlt}, props['children'])
    else:
        return el(MuiLink, {'href': props['to'],
                            'onClick': onClick}, props['children'])

