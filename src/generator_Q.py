import os
from typing import List, Dict, Tuple
from .config import *
from .prompt_template import SummaryPrompt, SubjectiveSummaryPrompt
from dataclasses import dataclass


@dataclass
class Story_Q:
    title: str
    chapters: Dict[str, str]
    summaries: Dict[str, str]

    def __iter__(self):
        return iter(self.chapters.items())
    

class Q_generator:
    def __init__(self, story_path):
        self.story = self._load_story(story_path)
        self.questions = {}

    def _load_story(self, story_path):
        with open(story_path, 'r') as f:
            original_story = f.read()
        sections = original_story.split('@@@')
        title, chapters = sections[0], sections[1:]
        story = Story_Q(title=title.strip(), chapters={f'chapter_{index+1}': chapter.strip() for index, chapter in enumerate(chapters)}, summaries={})
        return story
    
    def _load_summary(self, summary_path):
        if os.path.exists(summary_path):
            with open(summary_path, 'r') as f:
                original_summary = f.read()
            summaries = original_summary.split('@@@')
            self.story.summaries = {f'chapter_{index+2}': summary.strip() for index, summary in enumerate(summaries)}
        else:
            raise ValueError('Summary file not found.')
    
    def generate_summary_q(self):
        self.questions['summary'] = {}
        for chap_index, chapter in self.story:
            if chap_index == 'chapter_1':
                self.questions['summary'] = {chap_index: SummaryPrompt.format(chapter)}
            else:
                self.questions['summary'][chap_index] = SummaryPrompt.format( 'summary... '+ chapter)
    
    def generate_subjective_summary_q(self, characters):
        if not self.story.summaries:
            raise ValueError('Please load summary first.')
        self.questions['subjective_summary'] = {}
        for char in characters:
            self.questions['subjective_summary'][char] = {}
            for chap_index, chapter in self.story:
                if chap_index == 'chapter_1':
                    self.questions['subjective_summary'][char] = {chap_index: SubjectiveSummaryPrompt.format(chapter, char, char, char)}
                else:
                    self.questions['subjective_summary'][char][chap_index] = SubjectiveSummaryPrompt.format(self.story.summaries[chap_index] + chapter, char, char, char)
                

if __name__ == '__main__':
    path = StoryPath['Cinderella']['path']
    q_generator = Q_generator(story_path=f"{path}/story.txt")
    q_generator.generate_summary_q()
    # for chap in q_generator.questions['summary']:
    #     print('================================')
    #     print(q_generator.questions['summary'][chap])
    #     print('================================')
    q_generator._load_summary(summary_path=f"{path}/summary.txt")
    q_generator.generate_subjective_summary_q(characters=StoryPath['Cinderella']['characters'].values())
    import json
    with open(f"{path}/questions.json", "w") as json_file:
        json.dump(q_generator.questions, json_file, indent=4, ensure_ascii=False)
