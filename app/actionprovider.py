#!/usr/bin/env python
#from . import pluginMount
from .pluginmount import PluginMount
import requests

#PluginMount = pluginMount.PluginMount

class ActionProvider(metaclass=PluginMount):
    """
    Mount point for plugins which refer to actions that can be performed.

    Plugins implementing this reference should provide the following attributes:

---------------------------------------------------------------
    title       The text to be displayed, describing the action
    url         API Endpoint from which any data should be extracted from
    categories  A list of categories, which classify the plugin
    perform     The executing function
---------------------------------------------------------------
    """
    def __init__(self):
        #self.config = ConfigParser()
        #self.config.read("plugins.ini")
        pass


### Built in plugins

class ChuckNorrisJokes(ActionProvider):
    """Chuck Norris joke provider"""
    title = "Chuck Norris jokes"
    categories = ['joke', 'chuck', 'norris']
    url = "https://api.chucknorris.io/jokes/random"
    
    def perform(self):
        return requests.get(self.url).json()['value']

class SimplePlugin(ActionProvider):
    """Simple little plugin, says hello to the world"""
    title = "Simple Plugin Provider"
    categories = ["simple","hello","world"]
    url = None

    def perform(self):
        return "Hello World"


class iDatePlugin():
    import datetime 

    today = datetime.date.today()
    now = datetime.datetime.now()

    # Textual month, day and year
    def getDate(self):
        return self.today.strftime("%B %d, %Y")

    def getTime(self):
        return self.now.strftime("%H:%M")

    def perform(self):
        pass

class DatePlugin(ActionProvider, iDatePlugin):
    """DatePlugin"""
    title = "Some title"
    categories = ['date']
    url = None

    def perform(self):
        return self.getDate()

class TimePlugin(ActionProvider, iDatePlugin):
    """TimePlugin"""
    title = "Some title"
    categories = ['time']
    url = None

    def perform(self):
        return self.getTime()

class DefaultPlugin(ActionProvider):
    """Default Plugin"""
    title = "Default Plugin"
    categories = ['default']
    url = None

    def perform(self):
        return "I'm sorry, I don't know what to do. Please try a different command"

#class BoredPlugin(ActionProvider):
    #"""Activities to do when you're borde"""
    #title = "Activity suggestor for bored people"
    #categories = ['bored', 'activity']
    #url = "https://www.boredapi.com/api/activity"

    #def perform(self):
        #TODO
     #   pass


