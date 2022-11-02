# Copyright (c) 2022 Tuncay D.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.widget import base
from libqtile import hook

import subprocess


class Output(base.ThreadPoolText):
    """ ... """

    defaults = [
        ("update_interval", 
         60,
         "update time in seconds"),

        ("cmd",
         "date",
         "command line as a string or list of arguments to execute"),

        ("shell",
         True,
         "run command through a shell to enable piping and shell expansion"),

        ("text_before",
         "",
         "additional text to display before command output"),

        ("text_after",
         "",
         "additional text to display after command output"),
    ]


    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(Output.defaults)


    def _configure(self, qtile, bar):
        base.ThreadPoolText._configure(self, qtile, bar)

        self.text_before = str(self.text_before)
        self.text_after = str(self.text_after)

        self.add_callbacks({
            "Button1": self.cmd_force_update,
        })


    def poll(self):
        """ Run command and update from output. """

        self.run_process()
        return self.get_output()


    def run_process(self):
        """ Run command. """

        self.completed_process = subprocess.run(
            self.cmd,
            capture_output=True,
            text=True,
            shell=self.shell,
        )

        return self.completed_process


    def get_output(self):
        """ Extract output and format for bar. """

        output = self.completed_process.stdout.strip()
        output = self.text_before + output + self.text_after
        return str(output)

