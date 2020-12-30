from pkg.utils.console import write_stdout


class HtpResponse:
    _result: str = ''
    _error: str = ''

    def __init__(self, result='', error=''):
        self._result = result
        self._error = error

    def do(self):
        is_error = self._error != ''
        prefix = '? ' if is_error else '= '
        response = self._error if is_error else self._result
        write_stdout(f'{prefix}{response}\n')
        write_stdout('\n')
