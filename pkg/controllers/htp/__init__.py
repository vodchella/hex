import sys
from pkg.controllers import BaseController
from pkg.utils.console import write_stdout


class HtpController(BaseController):
    def run(self):
        for line in sys.stdin:
            cmd = line.strip('\n')
            if cmd == 'name':
                write_stdout('= PyHex\n')
            elif cmd == 'version':
                write_stdout('= 0.0.1\n')
            elif cmd == 'hexgui-analyze_commands':
                write_stdout('= \n')
            elif cmd.startswith('boardsize'):
                write_stdout('= \n')
            elif cmd.startswith('play'):
                write_stdout('= \n')
            elif cmd.startswith('genmove'):
                write_stdout('= \n')
            else:
                write_stdout(f'? unknown command: {cmd}\n')
            write_stdout('\n')
