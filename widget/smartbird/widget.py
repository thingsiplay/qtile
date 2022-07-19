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

import re
import pathlib


"""
To setup, you need to configure the widget itself:

    * set the "profile" to the main folder of your Thunderbirdird profile,
    in example: "~/.thunderbird/xxxxxx.default"
    * set the "update_interval", if default value is not sufficient

Next configure Thunderbird:

    * show "Unified Folders" by clicking on "...", on the right from
    "Folders"
    * open "Properties" on Inbox in Unified Folders (right mouse click on
    Inbox)
    * click button "Choose..." to open a dialog to select which mail
    accounts to include
    * scroll the list and enabled checkbox on those lines labled with
    "Inbox"
    * click "Ok" to close that dialog and "Update" to close previous
    dialog

Now the widget should be able to read new messages from activated mails
and even feeds. The widget will update after "update_interval" in seconds
or if left mouse click on widget. Additionally widget is updated when
Thunderbird client window gets or loses focus.
"""


class SmartBird(base.ThreadPoolText):
    """ Display number of new messages in Thunderbird Unified Folders. """

    defaults = [
        ("profile", None, "path to the Thunderbird profile"),
        ("mailbox", "Mail/smart mailboxes/Inbox.msf",
            "path to .msf mailbox file relative from Thunderbird profile"),
        ("update_interval", 900, "update time in seconds"),
        ("window_name", " - Mozilla Thunderbird",
            "update when focus enter or leave partially matching window name"),
    ]

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(SmartBird.defaults)

    def _configure(self, qtile, bar):
        base.ThreadPoolText._configure(self, qtile, bar)

        profile = pathlib.Path(self.profile).expanduser()
        mailbox = pathlib.Path(self.mailbox)
        self.file = pathlib.Path(profile / mailbox)

        self.add_callbacks({
            "Button1": self.cmd_force_update,
        })

        if self.window_name:
            hook.subscribe.client_focus(self.win_focus)
            # Will be updated to last focused window.
            self.last_client = None

    def poll(self):
        """ Scan mailbox for new messages """

        count = self.get_unreadmails(self.file.read_text())
        return str(count)

    def get_unreadmails(self, text):
        """ Read the last counter of unread mails. """

        # The regex searches for the last "A2=" entry, which contains the
        # number of unread mails. Everytime the number changes, a new entry is
        # added in the "Inbox.msf" file.
        # regex = r'1:\^9F\(\^A2=(\d+)'
        # Note: Sometimes it does not work if the part '1:\^9F' is included.
        regex = r'\(\^A2=(\d+)'
        count = re.findall(regex, text)[-1]
        if count is None:
            return 0
        else:
            return count

    def win_focus(self, client):
        """ Update only if new or last focused window matches. """

        if (self.window_name in client.name
                or self.window_name in self.last_client.name):
            self.cmd_force_update()
        self.last_client = client
