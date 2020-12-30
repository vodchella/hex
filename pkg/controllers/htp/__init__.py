import sys
from pkg.controllers import BaseController
from pkg.controllers.htp.response import HtpResponse


class HtpController(BaseController):
    def run(self):
        for line in sys.stdin:
            cmd = line.strip('\n')
            if cmd == 'name':
                resp = HtpResponse('PyHex')
            elif cmd == 'version':
                resp = HtpResponse('0.0.1')
            elif cmd == 'hexgui-analyze_commands':
                resp = HtpResponse()
            elif cmd.startswith('boardsize'):
                resp = HtpResponse()
            elif cmd.startswith('play'):
                resp = HtpResponse()
            elif cmd.startswith('genmove'):
                resp = HtpResponse()
            else:
                resp = HtpResponse(error=f'unknown command: {cmd}')
            resp.do()
