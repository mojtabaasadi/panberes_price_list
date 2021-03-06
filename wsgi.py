import cherrypy
import os,psycopg2
from jinja2 import Environment, FileSystemLoader
import jdatetime,datetime
from panberes_price.settings import DB


def pDate(val):
    dif = datetime.datetime.now() - val
    return jdatetime.datetime.fromgregorian(datetime=val).strftime(" %y-%m-%d %H:%M:%S") + (' --- ' + str(dif.days)+"روز پیش" if dif.days>0 else "" ) 


env = Environment(loader=FileSystemLoader('html'))
# if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
#     cherrypy.engine.start(blocking=False)
#     atexit.register(cherrypy.engine.stop)

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        conn = psycopg2.connect(**DB)
        cursor = conn.cursor()
        cursor.execute("select * from products")
        data = [{"id":pr[0],"title":pr[1],"price":pr[2],"updated_at":pr[3],"count":pr[4],"link":pr[5]} for pr in cursor.fetchall()]
        conn.close()
        env.filters['pDate'] = pDate
        tmpl = env.get_template('index.html')
        return tmpl.render(products=data)

config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    },
    '/assets': {
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'assets',
    }
}

cherrypy.quickstart(HelloWorld(), '/', config=config)
