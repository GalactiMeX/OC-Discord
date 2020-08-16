import socket
import discord
import threading

client = discord.Client()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 1337))
s.listen(5)


def background():
    global clientsocket, address
    while True:
        clientsocket, address = s.accept()
        print(address[0] + ':' + str(address[1]) + ' connected')


def foreground():
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('/execute_lua'):
            command_splitted = message.content.split(' ')
            if len(command_splitted) > 1:
                clientsocket.send(bytes(' '.join(command_splitted)[1:] + '\r\n', encoding="utf-8"))
                recv_data = str(clientsocket.recv(1024), encoding='utf-8')
                if recv_data.startswith('executed'):
                    sucess_embed = discord.Embed(title='Command executed.',
                                                 description=' '.join(recv_data.split(' ')[1:]), colour=0x20f200)
                    await message.channel.send(embed=sucess_embed)
                else:
                    print('Error: wrong recv_data ' + recv_data)
            else:
                error_embed = discord.Embed(title='Command executed with error.', description='Too few arguments.',
                                            colour=0xf2001c)
                await message.channel.send(embed=error_embed)


bg = threading.Thread(name='background', target=background)
fg = threading.Thread(name='foreground', target=foreground)

bg.start()
fg.start()
client.run('NzAyNTkwMTYwMDE3MDMxMjE4.Xu3wag.-iA1P9uCnqH9sRfAZmYeMvztwA4')
