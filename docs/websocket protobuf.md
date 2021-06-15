[download the compiler package](https://github.com/protocolbuffers/protobuf/releases)

```shell
protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/chat.proto
```

- `$SRC_DIR`: where your application's source code lives – the current directory is used if you don't provide a value
- `$DST_DIR`: where you want the generated code to go; often the same as `$SRC_DIR`
- `$SRC_DIR/chat.proto`: the path to your `.proto`

This generates `chat_pb2.py` in your specified destination directory.

`test_websocket_protobuf.py`:

```python
import asyncio

import websockets

import chat_pb2

pb = chat_pb2.Chat()
pb.content = "hello"
pb.type = "2"


async def hello(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send(pb.SerializeToString())
        response = await websocket.recv()
        print(response)


asyncio.get_event_loop().run_until_complete(
    hello('wss://xxx.com/ws'))

```

