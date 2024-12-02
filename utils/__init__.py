from pyrogram import Client


async def clear_tg_group_link(link: str) -> str:
    if "https://t.me/" in link:
        result = link.replace("https://t.me/", "")

    if "@" in link:
        result = link.replace("@", "")

    return result


async def get_chat(link):

    client = Client("+79283529546", api_id=27044267, api_hash="a7448d0befc9804176b9c917898d923a",
                    phone_number="+79283529546", workdir="sessions/")
    chat = await client.get_chat(link)
    await client.connect()
    await client.disconnect()

    return chat
