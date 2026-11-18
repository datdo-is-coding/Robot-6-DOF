import json
from pathlib import Path
w=Path(__file__).resolve().parent;c=w/'candidate';c.mkdir(exist_ok=True)
raw=(w/'before/src.ioc').read_bytes()
text=raw.decode();lines=text.splitlines();d=dict(x.split('=',1) for x in lines if x and not x.startswith('#') and '=' in x)
updates={'Mcu.Pin35':'PA0-WKUP','Mcu.PinsNb':'36','PA0-WKUP.Signal':'GPIO_Input','PA0-WKUP.Locked':'true','PA0-WKUP.GPIOParameters':'GPIO_Label','PA0-WKUP.GPIO_Label':'USB_VBUS','MxCube.Version':'6.18.1','MxDb.Version':'DB.6.0.181',
 'TIM1.Period':'4199','TIM1.Prescaler':'0','TIM1.DeadTime':'84','TIM1.Pulse-PWM\\ Generation4\\ No\\ Output':'2100'}
params=d['TIM1.IPParameters'].split(',')
for name in ['Prescaler','Pulse-PWM Generation4 No Output']:
 if name not in params:params.append(name)
updates['TIM1.IPParameters']=','.join(params)
for k,v in d.items():
 if k.startswith('TIM1.OCFastMode_PWM-'):updates[k]='TIM_OCFAST_DISABLE'
new=[]
for line in lines:
 key=line.split('=',1)[0]
 if key in updates:new.append(key+'='+updates.pop(key))
 else:new.append(line)
new.extend(k+'='+v for k,v in updates.items())
(c/'src.ioc').write_text('\n'.join(new)+'\n')
(w/'cubemx.requests.json').write_text(json.dumps([{'name':'cubemx_validate_ioc','arguments':{'path':str(c/'src.ioc')}}],indent=2)+'\n')
print('IOC candidate prepared: PA0 USB_VBUS, TIM1 20 kHz, deadtime 500 ns, CH4=2100')
