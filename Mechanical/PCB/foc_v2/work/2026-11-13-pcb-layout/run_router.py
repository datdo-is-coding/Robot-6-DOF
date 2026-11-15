import os,subprocess,json,time
from pathlib import Path
W=Path(__file__).resolve().parent;T=W/'tools'
env={**os.environ,'XDG_CONFIG_HOME':str(T/'config-home'),'XDG_STATE_HOME':str(T/'state'),'XDG_DATA_HOME':str(T/'data'),'XDG_CACHE_HOME':str(T/'cache')}
settings=json.loads((T/'config-home/freerouting/freerouting.json').read_text())
assert settings['usage_and_diagnostic_data']['disable_analytics']
java=(T/'java-path.txt').read_text().strip()
cmd=[java,'-Xmx4g','-Djava.awt.headless=true','-jar',str(T/'freerouting-2.5.0.jar'),'--gui.enabled=false','--api_server.enabled=false','--mcp_server.enabled=false','--usage_and_diagnostic_data.disable_analytics=true','--router.job_timeout=00:06:00','--router.fanout.max_passes=3','--router.optimizer.enabled=false','--router.optimizer.max_threads=3','--router.autorouter.max_passes=30','--router.neck_width_um=150','--router.automatic_neckdown=false','--router.strict_drc=false','--router.plane_as_obstacle=false','-de',str(W/'routing.dsn'),'-do',str(W/'routed.ses')]
with (W/'router.log').open('w') as f:
 start=time.monotonic();r=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=600)
(W/'router-result.json').write_text(json.dumps({'exit_code':r.returncode,'seconds':time.monotonic()-start,'ses_exists':(W/'routed.ses').exists(),'analytics_disabled':True},indent=2)+'\n')
print('Routing exited:',r.returncode,'session saved:',(W/'routed.ses').exists(),flush=True)
