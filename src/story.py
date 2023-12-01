import re
import websocket
import json
from typing import List, Dict, Tuple
from .config import *
from .prompt_template import SystemPrompt, PromtTemplate
from dataclasses import dataclass


@dataclass
class Story:
    title: str
    chapters: Dict[str, Tuple[List[str], str]]

    def __iter__(self):
        return iter(self.chapters.items())
    
class Storyteller:
    def __init__(self, story_path, summary_path):
        self.story = self._load_story(story_path, summary_path)
        self.port = ModelPort
        self.ip = "127.0.0.1"

    @staticmethod   
    def _sync_websocket_client(message, ip, port):

        ws_url = "ws://{}:{}".format(ip, port)

        # 创建 WebSocket 连接
        ws = websocket.WebSocket()

        # 连接到给定的 WebSocket 服务器
        ws.connect(ws_url)

        ws.send(message)

        response = ws.recv()
        ws.close()
        return response

    def _load_story(self, story_path, summary_path):
        with open(story_path, 'r') as f:
            original_story = f.read()
        with open(summary_path, 'r') as f:
            original_summary = f.read()
        summaries = original_summary.split('@@@')
        sections = original_story.split('@@@')
        title, chapters = sections[0], sections[1:]
        splitters = '(.*?(?:\n|。|？|！|……|…|\.|!|\?))'
        story = Story(title=title.strip(), chapters={})
        assert len(summaries) == len(chapters)

        for index, (chapter, summary) in enumerate(zip(chapters, summaries)):
            sentences = [x.strip() for x in re.findall(splitters, chapter) if x and not x.isspace() and x not in splitters]

            story.chapters[f'chapter_{index + 1}'] = (sentences, summary.strip())
        return story

    def tell_sentence(self):
        for chap, (sentences, summary) in self.story:
            for sentence in sentences:
                for char in sentence:
                    yield char, summary, chap
                yield '\n', summary, chap

    def answer(self, query, summary, talk_style, system_prompt=SystemPrompt):
        instruction = PromtTemplate.format(background=summary, talk_style=talk_style, user=query)
        message = json.dumps({"system_prompt": system_prompt, "instruction": instruction, "histories": []}, ensure_ascii=False)
        return self._sync_websocket_client(message, self.ip, self.port)