import json,os
from pathlib import Path
from stm32cubemx_mcp.cubemx import build_validation_script,run_cubemx_script
from stm32cubemx_mcp.ioc import IocDocument
from stm32cubemx_mcp.models import IocPlanRequest
from stm32cubemx_mcp.planning import prepare_ioc_changes
from stm32cubemx_mcp.settings import Settings
w=Path(__file__).resolve().parent
os.environ['CUBEMX_MCP_ALLOWED_ROOTS']=str(w.parent.parent)
os.environ['CUBEMX_MCP_CUBEMX_PATH']='/home/tuan/STM32CubeMX/STM32CubeMX'
os.environ['CUBEMX_MCP_CUBEMX_TIMEOUT_SECONDS']='120'
s=Settings.from_env()
request=IocPlanRequest.model_validate_json((w/'cubemx-plan-request.json').read_text())
plan,content=prepare_ioc_changes(request,s)
stage=w/'cubemx-roundtrip'; stage.mkdir(exist_ok=True)
source=stage/'src.ioc'; output=stage/'roundtrip.ioc'; source.write_bytes(content)
process=run_cubemx_script(build_validation_script(source,output),s,stage)
(stage/'process.json').write_text(process.model_dump_json(indent=2)+'\n')
assert process.succeeded,process
assert output.is_file()
roundtrip=IocDocument.parse(output.read_text()).entries
mismatches=[{'key':c.key,'expected':c.after,'actual':roundtrip.get(c.key)} for c in plan.changes if roundtrip.get(c.key)!=c.after]
print(json.dumps(mismatches,indent=2),flush=True)
(stage/'mismatches.json').write_text(json.dumps(mismatches,indent=2)+'\n')
