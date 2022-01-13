import asyncio
import HOSTandPORT

host = HOSTandPORT.host
port = HOSTandPORT.port


async def conn_proc(reader, writer):
    data = await reader.read(100)
    text = data.decode()

    print(text)
    writer.write(data)
    await writer.drain()

    writer.close()

async def main():
    server = await asyncio.start_server(conn_proc, host, port)
    await server.serve_forever()

loop = asyncio.get_event_loop()
task = loop.create_task(main())
loop.run_until_complete(task)
