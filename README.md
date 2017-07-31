# convodump
is a Python library **in development** for downloading your conversations from Facebook without having to wait for/go through their own process of requesting a backup. The main use case is for leaving facebook. You just start this, let it run overnight[1] and wake up the next day as a free person.

# requirements
I use Arch Linux and Python 3 to build it, the exact pacman/AUR packages are:
 - ipython (optional)
 - python
 - python-selenium
 - geckodriver
 - firefox
## other browsers
...are most like **not** supported, because Facebook renders differently in them and JavaScript messes things up (as is usual (*shots fired*)) and I only know how to turn it off in Firefox.
**However!** The code is structured so that you can pass any `browser` object to it and as long as it uses the `webdriver` API, there will be no problems, but please remember that the DOM queries are fragile, especially if the page loads things through JavaScript.
So with all that said, you should most likely just use Firefox.


# state
Currently it looks like you can dump raw html if you are lucky and know how to use Python, so I guess it's alpha.

# usage
TODO
For now, just read the source. It is planned to be usable by an average terminal user.

# hacking/helping out/major TODOs
See the comments in the source. The highest priority right now is the filtering framework. If you can dig around for how Facebook structures its HTML and find more quirks or solutions to them, that will be equally or possibly even more appreciated.

[1]: not necessarily, this thing is quite slow, even with a fast and stable connection and facebook has some quirks that might interrupt the download or otherwise mess things up
