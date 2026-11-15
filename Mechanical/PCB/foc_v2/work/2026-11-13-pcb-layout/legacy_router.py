import subprocess,pathlib,os,select
W=pathlib.Path(__file__).resolve().parent
java=(W/'tools/java-path.txt').read_text().strip()
d=W/'tools/legacy-config'
rfd,wfd=os.pipe()
with (W/'virtual-display.log').open('w') as v:
    server=subprocess.Popen([str(W/'tools/xvfb/usr/bin/Xvfb'),'-displayfd',str(wfd),'-screen','0','1280x900x24','-nolisten','tcp','-ac'],pass_fds=(wfd,),stdout=v,stderr=subprocess.STDOUT)
    os.close(wfd)
    try:
        assert select.select([rfd],[],[],8)[0],'Virtual display did not start'
        display=os.read(rfd,40).decode().strip();assert display.isdigit(),display
        (W/'virtual-display-number.txt').write_text(display+'\n')
        env={**os.environ,'DISPLAY':':'+display}
        cmd=[java,'-Xmx4g','-Duser.home='+str(d),'-jar',str(W/'tools/freerouting-1.9.0.jar'),'-de',str(W/'legacy.dsn'),'-do',str(W/'legacy.ses'),'-mp','50','-mt','0','-dct','1','-da','-dl']
        with (W/'legacy-router.log').open('w') as f:r=subprocess.run(cmd,env=env,cwd=d,stdout=f,stderr=subprocess.STDOUT,timeout=900)
        print('Legacy router exit',r.returncode,'SES',(W/'legacy.ses').exists(),flush=True)
    finally:
        server.terminate();server.wait(timeout=5);os.close(rfd)
