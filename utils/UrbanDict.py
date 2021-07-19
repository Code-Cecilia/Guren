
import aiohttp
import json
import re
import urllib


async def define(term):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://api.urbandictionary.com/v0/define?term={term}") as response:
            x = (await response.content.read()).decode("utf-8")
            # Thanks to CorpNewt for the idea, and his help in making this command work
            dict_object = json.loads(x)
            thing = dict_object
            list = thing.get('list')
            define1 = list[0]
            word = str(define1.get('word')).title()
            definition = str(define1.get('definition'))
            likes = define1.get('thumbs_up')
            dislikes = define1.get('thumbs_down')
            example = str(define1.get('example'))
            author = define1.get('author')

            pattern = r'\[(.+?)\]'

            result = set(re.findall(pattern, definition))
            for x in result:
                encoded = urllib.parse.quote(x)
                definition = definition.replace(f"[{x}]",
                                                f"__[{x}](https://www.urbandictionary.com/define.php?term={encoded})__")

            result2 = set(re.findall(pattern, example))
            for x in result2:
                encoded2 = urllib.parse.quote(x)
                example = example.replace(f"[{x}]",
                                          f"__[{x}](https://www.urbandictionary.com/define.php?term={encoded2})__")

            return word, definition, likes, dislikes, example, author
