import asyncio
import json
import os
import sys
import tomllib
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server, request_path, output_path = sys.argv[1:]
    requests = json.loads(Path(request_path).read_text())
    if server == 'kicad':
        cfg = json.loads(Path('/home/tuan/.gemini/config/mcp_config.json').read_text())['mcpServers']['kicad']
        cfg['env'].update(KCAA_TRUSTED_ROOTS=os.getcwd(), KICAD_SEARCH_PATHS=os.getcwd())
    else:
        cfg = tomllib.loads(Path('/home/tuan/.codex/config.toml').read_text())['mcp_servers'][server]
    params = StdioServerParameters(command=cfg['command'], args=cfg.get('args', []), env={**os.environ, **cfg.get('env', {}), 'PYTHONDONTWRITEBYTECODE': '1'})
    results = []
    with open(output_path + '.log', 'w') as log:
        async with stdio_client(params, errlog=log) as (read, write):
            async with ClientSession(read, write) as client:
                await client.initialize()
                for request in requests:
                    if request['name'] == '__list_tools__':
                        data = (await client.list_tools()).model_dump(mode='json', by_alias=True)
                    else:
                        response = await client.call_tool(request['name'], request.get('arguments', {}))
                        data = response.model_dump(mode='json', by_alias=True, exclude_none=True)
                    results.append({'request': request, 'result': data})
                    Path(output_path).write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
                    print(request['name'], 'ERROR' if data.get('isError') else 'OK', flush=True)
                    if data.get('isError'):
                        raise RuntimeError(data)
asyncio.run(asyncio.wait_for(main(), timeout=360))
