# GeneralAgent: From LLM to Agent

* GeneralAgent 是一个python库，可以快速搭建Agent应用，嵌入到你的业务中，或者通过 [AgentServer](https://github.com/CosmosShadow/AgentServer) 进行部署，快速给大规模用户提供Agent服务
* GeneralAgent 通过python代码解释器来调用工具，不依赖大模型的 function call
* GeneralAgent 支持序列化
* GeneralAgent 支持自我调用和堆栈记忆，请见[论文](./docs/paper/General_Agent__Self_Call_And_Stack_Memory.pdf)



## 安装

```bash
pip install GeneralAgent
```



## 使用

```python
from GeneralAgent.agent import Agent
from GeneralAgent import skills

agent = Agent.with_functions(role_prompt=f'你是一个小说家', new=True, continue_run=False)
# topic = skills.input('请输入小说的名称和主题: ')
topic = '小白兔吃糖不刷牙的故事'
summary = agent.run(f'小说的名称和主题是: {topic}，扩展和完善一下小说概要。要求具备文艺性、教育性、娱乐性。', return_type=str)
outline = agent.run('输出小说的章节名称和每个章节的概要，返回列表 [(chapter_title, chapter_summary), ....]', return_type=list)
chapters = []
for index, (title, summary) in enumerate(outline):
    chapter = agent.run(f'对于章节: {title}，{summary}. \n输出章节的详细内容', return_type=str)
    chapters.append(chapter)
with open('novel.md', 'w') as f:
    for index in range(len(outline)):
        f.write(f'### {outline[index][0]}\n{chapters[index]}\n\n')
skills.output('你的小说已经生成[novel.md](novel.md)')
```


## 论文

[General Agent：自调用和堆栈内存](./docs/paper/General_Agent__Self_Call_And_Stack_Memory.pdf)



## 加入我们

使用微信扫描下方二维码

<p align="center">
<img src="./docs/images/wechat.jpg" alt="wechat" width=400/>
</p>