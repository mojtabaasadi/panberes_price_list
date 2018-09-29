import cherrypy
import os,psycopg2,atexit
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('html'))
import jdatetime
def pDate(val):
    return jdatetime.datetime.fromgregorian(datetime=val).strftime(" %y-%m-%d %H:%M:%S")

if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
    cherrypy.engine.start(blocking=False)
    atexit.register(cherrypy.engine.stop)

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        conn = psycopg2.connect("dbname='cyynmluq' user='cyynmluq' host='pellefant.db.elephantsql.com' password='Sfdr_WCGjvIDoaVPyPkAd_qXrgkc0yQG'")
        cursor = conn.cursor()
        cursor.execute("select * from products")
        data = [{"id":pr[0],"title":pr[1],"price":pr[2],"available":pr[3],"updated_at":pr[4]} for pr in cursor.fetchall()]
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

application  = cherrypy.Application(HelloWorld(), '/', config=config)
