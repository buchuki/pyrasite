# This file is part of pyrasite.
#
# pyrasite is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyrasite is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyrasite.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2011, 2012 Red Hat, Inc.

import unittest

from pyrasite.inject import CodeInjector
from pyrasite.utils import run

class TestCodeInjection(unittest.TestCase):

    def test_injection(self):
        cmd = 'python -c "import time; time.sleep(0.5)"'
        p = run(cmd, communicate=False)[0]

        ci = CodeInjector(p.pid, verbose=True)
        ci.inject('pyrasite/payloads/helloworld.py')

        stdout, stderr = p.communicate()
        assert 'Hello World!' in stdout, "Code injection failed"

    def test_multithreaded_injection(self):
        cmd = [
            'import time, threading',
            'snooze = lambda: time.sleep(0.5)',
            'threading.Thread(target=snooze).start()',
            ]
        p = run('python -c "%s"' % ';'.join(cmd), communicate=False)[0]

        ci = CodeInjector(p.pid, verbose=True)
        ci.inject('pyrasite/payloads/helloworld.py')

        stdout, stderr = p.communicate()
        assert 'Hello World!' in stdout, "Multi-threaded code injection failed"

if __name__ == '__main__':
    unittest.main()
