from sanic import Sanic
from sanic.exceptions import ServerError
from sanic import response
import os
from sanic.log import logger
import sqlite3

loadpath= './upload'
database= './x/db_sqlite.db'

app = Sanic("hello_example")


@app.middleware('request')
async def print_on_request(request):
  with open("./upload/config.txt","r") as f:
    result = f.readlines()
    x = [x.replace('\n', '') for x in result]
  if request.ip not in x:
    print(request.ip)
    return response.redirect("/404")
  else:
    pass

# @app.route("/error")
# def i_am_ready_to_die(request):
#   raise ServerError("Something bad happened", status_code=500)

@app.route("/get_file")
async def get_file(request):
  dirs = os.listdir(loadpath)
  return response.json({"file_list": str(dirs)})


@app.route("/get_file/<filename>")
async def get_file_by_name(request,filename):
  try:
    con = sqlite3.connect(database)
    sql = '''SELECT status FROM filelist WHERE name = ? '''
    cur = con.cursor()
    cur.execute(sql, (filename,))
    returncode = cur.fetchone()
    if returncode == None:
        con.close()
        return response.redirect("/404")
    else:
        cur.execute("UPDATE filelist SET status = 2 WHERE name = ?", (filename,))
        con.commit()
        con.close()
        full_filename = loadpath+"/"+filename
        return await response.file_stream(full_filename)

  except Exception as e:
    return response.redirect("/404")


@app.route("/get_file_status/<filename>")
async def get_file_by_name(request,filename):
  #returncode  1:new 2:old 3:not exist 4:server error
  try:
    con = sqlite3.connect(database)
    sql = '''SELECT status FROM filelist WHERE name = ? '''
    cur = con.cursor()
    cur.execute(sql, (filename,))
    returncode = cur.fetchone()
    con.close()
    if returncode!= None:
      return response.json(returncode[0])
    else:
      return response.json(3)
  except Exception as e:
    return response.json(4)

  

@app.route("/put_file/<filename>", methods=['POST', 'GET'])
async def put_file_by_name(request,filename):
  full_filename = None
  try:
    con = sqlite3.connect(database)
    sql = '''SELECT status FROM filelist WHERE name = ? '''
    cur = con.cursor()
    cur.execute(sql, (filename,))
    returncode = cur.fetchone()
    if returncode == None:
        newdata = (1,filename)
        cur.execute("INSERT INTO filelist values(?,?)", newdata)
        con.commit()
    else:
        cur.execute("UPDATE filelist SET status = 1 WHERE name = ?", (filename,))
        con.commit()
    con.close()

    full_filename = loadpath+"/"+filename

    f = request.files.get("file")

    with open(full_filename, "wb") as fw:
      fw.write(f.body)

    return response.json('ok')
  except Exception as e:
    logger.info(e.__str__())

app.static('/static', './test.py')
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000,debug=True, access_log=True)
  #http://127.0.0.1:8000/tag