import cherrypy


class Root():
    def _cp_dispatch(self, vpath):
        if len(vpath) == 2:
            cherrypy.request.params['genericName'] = vpath.pop()
            cherrypy.request.params['root'] = vpath.pop()
            return self

    @cherrypy.expose
    def index(self, root, genericName):
        logger.debug(root)
        if root.lower() == 'generic':
            rows = set([str(row[0]) for row in DrugsList.findBrandName(cherrypy.request.db, genericName)])
            logger.debug(root + ": " + genericName)
            output = []
            for item in rows:
                match = re.search(rf'\b{genericName}\b', item)
                if match is None:
                    output.append(item)
            return f"{genericName}: {', '.join(output)}"
