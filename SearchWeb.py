import sublime
import sublime_plugin
import webbrowser
import re


def checkUrl(url):
    regex = re.compile(
        r'^(https?://)?'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)

def getSearchEngine():
    return getSettings().get("search_engine")

def makeUrl(search):
    if checkUrl(search) != None:
        if search.find("http") != 0:
            return '{}{}'.format('http://', search)
        return search
    else:
        return getSearchEngine().replace('%s', search)

def getSettings():
    return sublime.load_settings('SearchWeb.sublime-settings')

def convertPath():
    return getSettings().get('browser').replace('\\', '/')

class SearchWebCommand(sublime_plugin.WindowCommand):
    def run(self):
        window = self.window
        view = window.active_view()
        sel = view.sel()

        region1 = sel[0]
        search = view.substr(region1)

        search = makeUrl(search)

        webbrowser.get('{} %s'.format(convertPath())).open_new_tab(search)
        # webbrowser.open(search, 1, True)
