import os
import time
import logging
from pathlib import Path
from cherrypy.process import wspbus, plugins
from sqlalchemy import create_engine
from db.models import Base

logger = logging.getLogger('run')

class SAEnginePlugin(plugins.SimplePlugin):
    def __init__(self, bus):
        plugins.SimplePlugin.__init__(self, bus)
        self.sa_engine = None
        self.bus.subscribe("bind", self.bind)

    def start(self):
        p = Path.cwd()
        db = f"sqlite:///drugs.db"
        self.sa_engine = create_engine(os.environ.get('DB_URI', db))
        try:
            Base.metadata.create_all(self.sa_engine)
        except Exception as e:
            logger.warning('Failed to connect to db')
            time.sleep(30)
            logger.error('Second attempt to connect')
            Base.metadata.create_all(self.sa_engine)

    def stop(self):
        if self.sa_engine:
            self.sa_engine.dispose()
            self.sa_engine = None

    def bind(self, session):
        session.configure(bind=self.sa_engine)
