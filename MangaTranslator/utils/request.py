from httpx import Client
from aiowebsocket.converses import AioWebSocket

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

async def ws_connect(path):
    """path: foo/bar"""
    
    async with AioWebSocket(
        f'wss://{backend_host}/{path}',
        timeout=10
    ) as ws:
        aws = ws.manipulator
        while True:
            yield await aws.receive(text=True)
    