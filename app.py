from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import sqlite3, json, os
from datetime import datetime
from zoneinfo import ZoneInfo

DB = os.environ.get('RAID_DB', 'raid.db')
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON'); return c
with db() as c:
 c.executescript('CREATE TABLE IF NOT EXISTS raids(id INTEGER PRIMARY KEY, name TEXT NOT NULL, archived INTEGER NOT NULL DEFAULT 0); CREATE TABLE IF NOT EXISTS players(id INTEGER PRIMARY KEY, raid_id INTEGER NOT NULL REFERENCES raids(id), name TEXT NOT NULL); CREATE TABLE IF NOT EXISTS mistakes(id INTEGER PRIMARY KEY, player_id INTEGER NOT NULL REFERENCES players(id), day TEXT NOT NULL, created TEXT NOT NULL);')
class Handler(BaseHTTPRequestHandler):
 def send(self, status, data, typ='application/json; charset=utf-8'):
  data=data if isinstance(data,bytes) else json.dumps(data,ensure_ascii=False).encode(); self.send_response(status); self.send_header('Content-Type',typ); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
 def do_GET(self):
  if self.path=='/':
   with open(os.path.join(os.path.dirname(__file__),'index.html'),'rb') as f:self.send(200,f.read(),'text/html; charset=utf-8')
  elif self.path=='/api/raids':
   with db() as c:
    raids=[dict(x) for x in c.execute('SELECT * FROM raids ORDER BY id DESC')]
    for r in raids:
     r['players']=[dict(x) for x in c.execute('SELECT p.id,p.name,COUNT(m.id) total FROM players p LEFT JOIN mistakes m ON p.id=m.player_id WHERE p.raid_id=? GROUP BY p.id ORDER BY p.id',(r['id'],))]
     r['days']=[dict(x) for x in c.execute('SELECT m.day,p.name,COUNT(*) total FROM mistakes m JOIN players p ON p.id=m.player_id WHERE p.raid_id=? GROUP BY m.day,p.id ORDER BY m.day DESC,p.id',(r['id'],))]
   self.send(200,raids)
  else:self.send(404,{'error':'No encontrado'})
 def do_POST(self):
  try:
   n=int(self.headers.get('Content-Length','0'))
   if n>100000: raise ValueError('Solicitud demasiado grande')
   d=json.loads(self.rfile.read(n)); path=urlparse(self.path).path
   with db() as c:
    if path=='/api/create':
     name=str(d.get('name','')).strip(); players=[str(x).strip() for x in d.get('players',[]) if str(x).strip()]
     if not name or not players: raise ValueError('Introduce un nombre y al menos un integrante')
     rid=c.execute('INSERT INTO raids(name) VALUES (?)',(name,)).lastrowid
     c.executemany('INSERT INTO players(raid_id,name) VALUES (?,?)',[(rid,p) for p in players])
    elif path=='/api/mistake':
     now=datetime.now(ZoneInfo('Europe/Madrid')); pid=int(d['player_id'])
     row=c.execute('SELECT raids.archived FROM players JOIN raids ON raids.id=players.raid_id WHERE players.id=?',(pid,)).fetchone()
     if not row or row['archived']: raise ValueError('Raid no disponible')
     c.execute('INSERT INTO mistakes(player_id,day,created) VALUES (?,?,?)',(pid,now.date().isoformat(),now.isoformat()))
    elif path=='/api/undo':
     pid=int(d['player_id']); row=c.execute('SELECT raids.archived FROM players JOIN raids ON raids.id=players.raid_id WHERE players.id=?',(pid,)).fetchone()
     if not row or row['archived']: raise ValueError('Raid no disponible')
     c.execute('DELETE FROM mistakes WHERE id=(SELECT id FROM mistakes WHERE player_id=? ORDER BY id DESC LIMIT 1)',(pid,))
    elif path=='/api/archive': c.execute('UPDATE raids SET archived=1 WHERE id=?',(int(d['raid_id']),))
    else: return self.send(404,{'error':'No encontrado'})
   self.send(200,{'ok':True})
  except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:self.send(400,{'error':str(e)})
if __name__=='__main__':
 print('Abre http://localhost:8000'); HTTPServer(('127.0.0.1',8000),Handler).serve_forever()
