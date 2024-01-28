from httpx import Client
from aiowebsocket.converses import AioWebSocket
from json import loads as __json_loads

backend_host = "api.cotrans.touhou.ai"

__session__ = Client(
    base_url=f'https://{backend_host}',
    # proxies={ # for debug
    #     'http://':'http://192.168.1.103:9000',
    #     'https://':'http://192.168.1.103:9000'
    # },
    # verify=False,
    timeout=10000
)

#可使用绝对/相对路径
PUT = __session__.put
GET = __session__.get  

async def WS_WAIT_JSON(path):
    """path: foo/bar"""
    async with AioWebSocket(
        f'wss://{backend_host}/{path}',
    ) as ws:
        aws = ws.manipulator
        while True:
            try:
                s=await aws.receive(text=True)
                if s is not None:
                    yield __json_loads(s)
            except UnicodeDecodeError as e:
                if b'Done' in s:
                    break
            except Exception as e:
                print('uncought error',e)
                break