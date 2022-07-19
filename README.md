# Things I Qtile

This is a repository about stuff for Qtile.

* Author: Tuncay D.
* Source: https://github.com/thingsiplay/qtile
* License: [MIT License](LICENSE)

## Description

This repository is dedicated to share the little things I create for the tiling
window manager [Qtile](https://github.com/qtile/qtile) on Linux. These can be
in example settings, media, documents, addons or widgets to enhance and change
it's functionality.

## Installation

The simplest way is to clone the repo and just use the stuff you need.
Following command will download the repo and save it in a folder "thingsiplay"
in your Qtile directory:

```
git clone "https://github.com/thingsiplay/qtile" ~/.config/qtile/thingsiplay
```

Now the stuff is provided under the namespace "thingsiplay". You can import any
specific part of it in your "config.py" like this widget in example:

```
from thingsiplay.widget import smartbird
```

What the imported package provides will vary and depends on it's type. Read the
README.md of the package to learn what it does and how to use it.
