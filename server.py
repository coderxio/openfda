import re
import cherrypy
from cherrypy.process import wspbus, plugins
from connect_db import Drugs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class DrugsList(Drugs):
    def __init__(self):
        Drugs.__init__(self)
    
    @staticmethod
    def findBrandName(session, genericName):
        return session.query(DrugsList.brand_name) \
                .filter(DrugsList.generic_name.like('%' + genericName + '%'))

class SAEnginePlugin(plugins.SimplePlugin):
    def __init__(self, bus):
        plugins.SimplePlugin.__init__(self, bus)
        self.sa_engine = None
        self.bus.subscribe("bind", self.bind)
    
    def start(self):
        self.sa_engine = create_engine('mysql+pymysql://admin:admin@db:3306/drugs')
    
    def stop(self):
        if self.sa_engine:
            self.sa_engine.dispose()
            self.sa_engine = None
    
    def bind(self, session):
        session.configure(bind=self.sa_engine)

class SATool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'on_start_resource',
                               self.bind_session,
                               priority=20)
    
        self.session = scoped_session(sessionmaker(autoflush=True, autocommit=False))

    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('on_end_resource',
                                       self.commit_transaction,
                                       priority=80)

    def bind_session(self):
        cherrypy.engine.publish('bind', self.session)
        cherrypy.request.db = self.session

    def commit_transaction(self):
        cherrypy.request.db = None
        try:
            self.session.commit()
        except:
            self.session.rollback()
        finally:
            self.session.remove()


class Root():
    def _cp_dispatch(self, vpath):
        if len(vpath) == 1:
            cherrypy.request.params['genericName'] = vpath.pop()
            return self

    @cherrypy.expose
    def index(self, genericName):
        rows = set([str(row[0]) for row in DrugsList.findBrandName(cherrypy.request.db, genericName)])
        output = []
        for item in rows:
            match = re.search(rf'\b{genericName}\b', item)
            if match is None:
                output.append(item)
        return f"{genericName}: {', '.join(output)}"


def main():
    SAEnginePlugin(cherrypy.engine).subscribe()
    cherrypy.tools.db = SATool()
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.tree.mount(Root(), '/', {'/': {'tools.db.on': True}})
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    main()
