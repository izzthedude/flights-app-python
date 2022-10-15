import simplejson as json
import mariadb
from flask import Blueprint

from _env import config

airports = Blueprint('airports', __name__)


@airports.route('/api/airports', methods=['GET'])
def index():
   conn = mariadb.connect(**config)
   cur = conn.cursor()
   cur.execute("select * from airports order by airport") 
   row_headers=[x[0] for x in cur.description] 
   rv = cur.fetchall()
   json_data=[]
   for result in rv:
        json_data.append(dict(zip(row_headers,result)))
   return json.dumps(json_data)