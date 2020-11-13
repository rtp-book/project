import time
from common.pyreact import ReactGA
from common.jsutils import console

# __pragma__ ('skip')
from common import require, window, JSON
# __pragma__ ('noskip')


polyfill = require("@babel/polyfill")  # required by async/await


# __pragma__ ('kwargs')
async def fetch(url, callback=None, **kwargs):
    ReactGA.event({'category': 'api', 'action': 'request', 'label': url})
    t_start = time.time()
    on_error = kwargs.pop('onError', None)
    method = kwargs.pop('method', 'get')
    try:
        if method == 'POST' or method == 'DELETE':
            data = kwargs.pop('data', None)
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

        if response.status != 200:
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

