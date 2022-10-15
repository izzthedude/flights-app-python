import simplejson as json
import mariadb
from flask import Blueprint

from _env import config

airlines = Blueprint('airlines', __name__)


@airlines.route('/api/airlines', methods=['GET'])
def index():
   conn = mariadb.connect(**config)
   cur = conn.cursor()
   cur.execute("select * from airlines order by airline")
   row_headers=[x[0] for x in cur.description] 
   rv = cur.fetchall()
   json_data=[]
   for result in rv:
        json_data.append(dict(zip(row_headers,result)))
   return json.dumps(json_data)