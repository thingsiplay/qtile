# Output

A Qtile widget to display output from scripts or shell commands.

## Description

This widget is a plugin for Qtile, which executes shell commands or scripts.
The stdout output will be displayed as text on the bar.

The base idea of this widget was added to Qtile as [GenPollCommand](https://docs.qtile.org/en/latest/manual/ref/widgets.html#genpollcommand).

### Why this new widget?

There is already a `widget.GenPollText` which can do the same things as this
widget does, when configured correctly. Downside of it is the requirement of
understanding how Python processes are setup to run. Especially newcomers to
Python and Qtile can struggle with this. That's when this widget
`output.Output` comes into play. It is optimized for the task to run and
display output of shell commands and scripts only. That and the naming of the
options makes it easier to understand and more simple to configure than the
general purpose GenPollText widget.

## How to use

The widget runs and updates displayed text every `update_interval` in seconds.
A default action for left mouse button is setup as a mouse button callback to
run the update procedure instantly. The most important configuration to set is
`cmd`.  It defines what shell command or script to execute. Your command or
script is self responsible to output just a single line, because the bar of
Python usually displays only one line. Surrounding newline and whitespace
characters are stripped out automatically.

### Import widget

Assuming the repository was cloned to "~/.config/qtile/thingsiplay", then you
just need to:

```
from thingsiplay.widget import output
```

which provides you a widget named `Output` for the `bar` section. You can
use it like this:

```
output.Output(
    cmd = 'date',
),
```

### Configure widget

There is only one required setting for the widget to make, the command to
execute: `cmd`. This can be a simple string like `'date "+%+4Y-%m-%d"'` or a
list of strings, where each argument is broken up like this `['date',
'+%+4Y-%m-%d']`.

If you like, you can also disable the shell extension with `shell = False`
(enabled by default). Running a command with the shell enabled will allow
piping and shell expansion like `~` to home directory. The default
`update_interval` is set to `60` seconds. The options `text_before` and
`text_after` are very simple text strings to add text before and after the
command output when displaying it on the bar. These are bit easier to explain
and understand for newcomers.

### Examples

#### Basic usage:

```
output.Output(
    update_interval = 1,
    cmd = "date --rfc-3339=seconds",
),
```

Example output on the bar: `2022-11-02 00:43:39+01:00`

#### List of arguments

Or same command broken up into a list. With a list of arguments, Python will
ensure to enclose each argument in correct quotation marks:

```
output.Output(
    update_interval = 1,
    cmd = ['date', '--rfc-3339=seconds'],
),
```

Example output on the bar: `2022-11-02 00:43:39+01:00`

#### Without shell extensions

Disable shell extensions when it's not needed. Also in some cases disabling the
shell could be required, as in my next example (at least for me it was).

```
output.Output(
    update_interval = 60 * 4,
    cmd = ['qtile', '-v'],
    shell = False,
),
```

Example output on the bar: `0.21.1.dev118+g1748e0d7`

#### Additional text and formatting

Add some fixed text before and after the command output. This can include some
pango parkup to format it further.

```
output.Output(
    cmd = "du -hs ~/.local/share/Trash | grep -oE '[0-9]+.'",
    text_before = 'Trash: <i>',
    text_after = '</i>',
),
```

Example output on the bar: `Trash:` *`69M`*

