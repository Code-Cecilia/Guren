import aiohttp
import ast


async def get_quote():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://zenquotes.io/api/random") as response:
            response_list = (await response.content.read()).decode('utf-8')
            response_list = ast.literal_eval(response_list)
            response_dict = response_list[0]
            actual_quote = response_dict.get('q')
            actual_author = response_dict.get('a')
            quote_string = f"_{actual_quote}_ - {actual_author}"
            return quote_string
