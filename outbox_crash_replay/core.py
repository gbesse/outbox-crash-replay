import tempfile,sqlite3,subprocess,sys,os,signal,selectors
from pathlib import Path
WORKER=r"""import sqlite3,sys,threading
root,stage,mode=sys.argv[1:];db=sqlite3.connect(root+'/domain.db');db.execute('BEGIN');db.execute('INSERT INTO domain VALUES(1)');db.execute('INSERT INTO outbox VALUES(1,0)')
def pause():
 print('checkpoint',flush=True);threading.Event().wait(60)
if stage=='before_commit':pause()
db.commit()
if stage=='after_commit':pause()
effects=sqlite3.connect(root+'/effects.db');effects.execute('INSERT OR IGNORE INTO effects(event_id) VALUES(1)');effects.commit();effects.close()
if stage=='after_delivery_before_ack':pause()
"""
def scenario(stage,mode):
 with tempfile.TemporaryDirectory(prefix='owned-outbox-')as tmp:
  root=Path(tmp)
  with sqlite3.connect(root/'domain.db')as db:db.executescript('CREATE TABLE domain(id INTEGER PRIMARY KEY); CREATE TABLE outbox(id INTEGER PRIMARY KEY,acked INTEGER NOT NULL)')
  with sqlite3.connect(root/'effects.db')as db:
   db.execute('CREATE TABLE effects(seq INTEGER PRIMARY KEY,event_id INTEGER'+(' UNIQUE'if mode=='idempotent'else'')+')')
  env={k:os.environ[k]for k in ('PATH','SYSTEMROOT','WINDIR','TMPDIR','LANG')if k in os.environ};child=subprocess.Popen([sys.executable,'-I','-c',WORKER,tmp,stage,mode],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=env)
  try:
   with selectors.DefaultSelector()as selector:
    selector.register(child.stdout,selectors.EVENT_READ)
    if not selector.select(15)or child.stdout.readline().strip()!='checkpoint':raise ValueError('worker_checkpoint')
   child.kill();stdout,stderr=child.communicate(timeout=5)
   if child.returncode!=-signal.SIGKILL or stderr:raise ValueError('worker_termination')
  finally:
   if child.poll()is None:child.kill();child.communicate(timeout=5)
  with sqlite3.connect(root/'domain.db')as db:
   domain_count=db.execute('SELECT COUNT(*) FROM domain').fetchone()[0];pending=db.execute('SELECT id FROM outbox WHERE acked=0 ORDER BY id').fetchall()
   with sqlite3.connect(root/'effects.db')as effects:
    before=effects.execute('SELECT COUNT(*) FROM effects').fetchone()[0]
    for(event_id,)in pending:
     effects.execute('INSERT OR IGNORE INTO effects(event_id) VALUES(?)',(event_id,));effects.commit();db.execute('UPDATE outbox SET acked=1 WHERE id=?',(event_id,));db.commit()
    after=effects.execute('SELECT COUNT(*) FROM effects').fetchone()[0]
   acked=db.execute('SELECT COUNT(*) FROM outbox WHERE acked=1').fetchone()[0]
  return {'stage':stage,'consumer':mode,'termination_signal':'SIGKILL','domain_rows_after_recovery':domain_count,'pending_before_recovery':len(pending),'effects_before_recovery':before,'effects_after_recovery':after,'acked_after_recovery':acked}
def run(data):
 stages=data.get('stages',['before_commit','after_commit','after_delivery_before_ack']);modes=data.get('consumers',['naive','idempotent'])
 if os.name!='posix'or not isinstance(stages,list)or not isinstance(modes,list)or not stages or not modes or len(stages)>3 or len(modes)>2 or any(x not in ('before_commit','after_commit','after_delivery_before_ack')for x in stages)or any(x not in ('naive','idempotent')for x in modes):raise ValueError('scenarios')
 return {'scenarios':[scenario(s,m)for s in stages for m in modes],'model':'actual_sigkill_sqlite_transaction_outbox_separate_consumer_ledger_not_power_loss_test'}
