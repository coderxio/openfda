import cherrypy
import configparser
from cherrypy.process import wspbus, plugins
from connect_db import Drugs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


# Config settings under [database] section in settings.ini
def load_config():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    return config['database']['use_docker']


class DrugsList(Drugs):
    def __init__(self):
        Drugs.__init__(self)
    
    @staticmethod
    def listDrugs(session):
        return session.query(DrugsList.brand_name) \
                .filter(DrugsList.brand_name != 'lisinopril').filter(DrugsList.generic_name == 'lisinopril')

class SAEnginePlugin(plugins.SimplePlugin):
    def __init__(self, bus):
        plugins.SimplePlugin.__init__(self, bus)
        self.sa_engine = None
        self.bus.subscribe("bind", self.bind)
    
    def start(self):
        settings = load_config()
        if settings == 'yes':
            self.sa_engine = create_engine('mysql+pymysql://admin:admin@db:3306/drugs')
        else:
            self.sa_engine = create_engine('sqlite://')
    
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
    @cherrypy.expose
    def index(self):
        rows = [str(row[0]) for row in DrugsList.listDrugs(cherrypy.request.db)]
        n1 = '\n'
        return f"Lisinopril brand names: {n1.join(rows)}"


def main():
    SAEnginePlugin(cherrypy.engine).subscribe()
    cherrypy.tools.db = SATool()
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.tree.mount(Root(), '/', {'/': {'tools.db.on': True}})
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    main()
