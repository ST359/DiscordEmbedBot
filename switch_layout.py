

EN = 'qwertyuiop[]asdfghjkl;\'\zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>?'
RU = 'йцукенгшщзхъфывапролджэ\ячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,'



async def switch_en_to_ru(ctx):
    command_message = ctx.message
    if command_message.reference:
        message_to_translate = await command_message.channel.fetch_message(command_message.reference.message_id)
        message_autor = message_to_translate.author.display_name
        text_to_translate: str = message_to_translate.content
        translated_text = ''
        for chr in text_to_translate:
            if chr in EN:
                translated_text+= RU[EN.index(chr)]
            else:
                translated_text+=chr
        await ctx.send(f'**{message_autor}**:\n\n{translated_text}')
    else:
        pass
