import discord
from discord.ext.commands import Bot
from message_url_processing import make_url_embeddable, extract_url_from_message, does_contain_urls, \
    replace_urls_with_embeddables
from video_convertion import convert_video
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = Bot(command_prefix="!", intents=intents)
is_enabled = True


@client.event
async def on_message(message):
    global is_enabled
    if message.author == client.user:
        return

    if message.content == '!shut':
        if is_enabled:
            await message.channel.send('Disabled. To enable type "!run"')
            is_enabled = False
    elif message.content == '!run':
        if not is_enabled:
            await message.channel.send('Enabled. To disable type "!shut"')
            is_enabled = True
    if message.content == '!convert' and is_enabled:
        if message.attachments[0]:
            attach = message.attachments[0]
            if 'video' in attach.content_type:
                await attach.save(f'video_to_convert/{attach.filename}')
                convert_video(f'video_to_convert/{attach.filename}')
                file = discord.File('converted_vids/output.mp4')
                await message.channel.send(file=file)
                os.remove(f'video_to_convert/{attach.filename}')
                os.remove('converted_vids/output.mp4')

    if is_enabled:
        message_str: str = message.content
        message_replied_to = message.reference
        if does_contain_urls(message_str):
            raw_urls, parsed_urls = extract_url_from_message(message_str)
            embeddable_urls = make_url_embeddable(parsed_urls)
            new_message_content = replace_urls_with_embeddables(message_str, raw_urls, embeddable_urls)
            new_message = '**' + message.author.display_name + '**' + '\n' + '\n' + new_message_content
            if message_replied_to is not None:
                await message.channel.send(content=new_message, reference=message_replied_to, mention_author=False)
                await message.delete()
            else:
                await message.channel.send(new_message)
                await message.delete()


client.run(os.getenv('TOKEN'))
