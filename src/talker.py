from .story import Storyteller
from .character import CharactersLoader
from .config import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == '__main__':
    import time
    import sys
    story_config = StoryPath['Cinderella']
    storyteller = Storyteller(story_config['path'] + '/story.txt', story_config['path'] + '/summary.txt')
    characters = CharactersLoader(story_config).characters
    count = 0
    queries = \
    {
        14: {'cinderella': "灰姑娘，你为什么能忍你的继母和姐妹这么久，为什么不奋起反抗，或者告诉你的父亲？", "stepmother": "为什么你要这么对待灰姑娘？她明明是一个这么善良的人！"},
        18: {'stepsister': "姐姐，你为什么要让你的继父带这么名贵的礼物回来？"},
        19: {'cinderella': "灰姑娘，为什么让你父亲带回来一根树枝而不是其它的礼物？"},
        67: {'stepmother': "继母，你为什么要不让灰姑娘去舞会，她明明完成了你交代的事情，你怎么这么恶毒？"},
        82: {'cinderella': "灰姑娘，你为什么不告诉王子你的名字，并且不让他送你回家？"},
        78: {'prince': "王子，你为什么老是和同一位姑娘跳舞，是只看上了她的美貌嘛？"},
        101: {'prince': "王子，为什么要砍梨树，树树做错了什么！过分分！"},
        112: {'cinderella': '灰姑娘，你怎么把金舞鞋弄丢了，你不会是故意的吧，其实你内心也憧憬成为王妃吧？'},
        113: {'prince': '王子，你不知道很多人脚的大小都一样嘛，你这不是刻舟求剑嘛，你怎么保证你能找到和你跳舞的女人？'},
        118: {'stepmother': "继母，你怎么能砍掉你大女儿的脚趾和小女儿的脚后跟呢？就算成为王妃，这个能和女儿的健康相比嘛？"},
        156: {'cinderella': "灰姑娘，你为什么不报复你的继母和姐妹呢？他们明明对你很坏，你为什么杀了她们？"}
    }
    for char, summary, chap in storyteller.tell_sentence(): 
        sys.stdout.write(bcolors.OKGREEN + char + bcolors.ENDC)
        if char == '\n':
            if count in queries:
                for character_name, query in queries[count].items():
                    sys.stdout.write(bcolors.FAIL + f'==========={character_name}: {query}============\n'+ bcolors.ENDC)
                    sub_summary = characters[character_name].summary[chap]
                    system_prompt, talk_style, background, user = characters[character_name].config['system'], characters[character_name].config['talk_style'], characters[character_name].config['background'], characters[character_name].config['user']
                    background = background.format(context=sub_summary)
                    user = user.format(query=query)
                    resp = storyteller.answer(query=user, summary=background, talk_style=talk_style, system_prompt=system_prompt)
                    sys.stdout.write(bcolors.OKBLUE + resp + "\n" + bcolors.ENDC)
                    sys.stdout.write(bcolors.FAIL + '=========================================\n'+ bcolors.ENDC)
            count += 1

        sys.stdout.flush()

    sys.stdout.write('\033[0m')  #在结束时重置颜色
