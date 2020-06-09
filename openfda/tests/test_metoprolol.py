import cherrypy
from cherrypy.test import helper

from api import views
from api.plugins import SAEnginePlugin
from api.tools import SATool


class IndexViewTest(helper.CPWebCase):
    @staticmethod
    def setup_server():
        SAEnginePlugin(cherrypy.engine).subscribe()
        cherrypy.tools.db = SATool()
        cherrypy.tree.mount(views.Root(), '/', {'/': {'tools.db.on': True}})

    def test_something(self):
        res = self.getPage('/generic/metoprolol/')
        self.assertStatus('200 OK')
        print(res)
        assert False
