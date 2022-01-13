import asyncio
import HOSTandPORT

host = HOSTandPORT.host
port = HOSTandPORT.port


async def client(host, port):
    reader, writer = await asyncio.open_connection(host, port)

    text = 'It is message for test'

    writer.write(text.encode())
    await writer.drain()

    data = await reader.read(100)
    print("Выполнена передача текста")
    writer.close()
    await writer.wait_closed()

asyncio.run(client(host, port))
