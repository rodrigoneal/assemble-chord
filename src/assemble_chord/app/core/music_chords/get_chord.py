import httpx


async def get_chord_in_banana(chord_name):
    async with httpx.AsyncClient() as client:
        BASE_URL = "https://banana-s3.b-cdn.net/chordapi/search2"
        return await client.get(BASE_URL, params={"v": "5", "q": chord_name})
