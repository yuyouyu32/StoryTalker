SummaryPrompt ="""[{}]
请根据上述旁白故事，总结一篇完整的故事梗概。"""

SubjectiveSummaryPrompt = """[{}]
请从上述旁白故事中，以{}角色的视角总结故事。利用想象力描述{}角色在事件中的心理活动，考虑该角色的性格和经历，用第一人称视角展示这个总结。如果该角色在旁白故事中没有出现，则回复“该角色并未出现在这段故事中”。"""

SystemPrompt = "你是由Lilith Game训练的小莉, 你是一个非常善于从故事中总结信息并回答用户问题的AI，下面的问题请用中文回答。"

PromtTemplate = """{background}{talk_style}{user}"""
