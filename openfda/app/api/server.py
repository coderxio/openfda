import cherrypy
from api.plugins import SAEnginePlugin
from api.tools import SATool
from api.views import Root


def start_server():
    SAEnginePlugin(cherrypy.engine).subscribe()
    cherrypy.tools.db = SATool()
    cherrypy.tree.mount(Root(), '/', {'/': {'tools.db.on': True}})
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.engine.start()
    cherrypy.engine.block()
