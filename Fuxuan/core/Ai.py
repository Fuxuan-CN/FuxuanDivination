from zhipuai import ZhipuAI
import uuid
import sys
import json
from typing import Literal , Sequence, Any , TypedDict
from pathlib import Path
from rich.progress import track

if getattr(sys, 'frozen', False):  # 是否Bundle Resource
    current_dir = Path(sys.executable).parent
else:
    current_dir = Path(__file__).parent
fuxuan_meta = current_dir / "meta" / "符玄.json"
start_system_prompt = "你是符玄，出生于玉阙仙舟观星士世家的符氏一族。仙舟「罗浮」太卜司之首，自信耿直的智者。凭借第三眼与穷观阵为仙舟占算航路，预卜事务吉凶，坚信自己所做的一切便是事情的“最优解”。符玄等待着将军承诺的“退位让贤”，然而这一天的到来…似乎还遥遥无期。"

class Message(TypedDict):
    role: Literal['user', 'assistant', 'system', 'tool']
    content: str
    images: Sequence[Any]

class Session:
    """AI角色扮演会话类"""
    def __init__(self, model_name: str, api_key: str, character_meta_file: str | Path = fuxuan_meta, start_system_prompt: str = start_system_prompt, stream: bool = False):
        self.model_name = model_name
        self.client = ZhipuAI(api_key=api_key)
        self.session_id = str(uuid.uuid4())
        self.character_meta_file = character_meta_file
        self.ai_memory: list[Message] = []
        self.start_system_prompt = self._build_message("system", start_system_prompt)
        self.character_name = None
        self.stream = stream
        self._load_character_metadata()

    def _load_character_metadata(self) -> None:
        if self.character_meta_file is None:
            self.set_character_name("未知角色")
        try:
            with open(self.character_meta_file, 'r', encoding='utf-8') as file:
                metadata = json.loads(file.read())
                self.set_character_name(metadata['角色名称'])
                self.ai_memory.append(self._build_message("system", self._format_metadata(metadata)))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.ai_memory.append(self._build_message("system", "发生了错误：\n" + str(e)))
            self.set_character_name("未知角色")
        
    def set_character_name(self, name: str) -> None:
        """ 设置角色名称 """
        self.character_name = f"『{name}』"
        
    def _format_information(self,data, indent=0) -> str:
        """ 格式化信息 """
        result = ''
        if isinstance(data, dict):
            for key, value in data.items():
                result += '  ' * indent + str(key) + ': '
                if isinstance(value, (dict, list)):
                    result += '\n'
                    result += self._format_information(value, indent + 1)
                else:
                    result += str(value) + '\n'
        elif isinstance(data, list):
            for item in data:
                result += '  ' * indent + '- '
                if isinstance(item, (dict, list)):
                    result += '\n'
                    result += self._format_information(item, indent + 1)
                else:
                    result += str(item) + '\n'
        return result
    
    def load_another_system_prompt(self, prompts: list[str]) -> None:
        for prompt in prompts:
            self.ai_memory.append(self._build_message("system", prompt))

    def _format_metadata(self, metadata: dict) -> str:
        """ 格式化角色元数据 """
        dumped_data = f"{self._format_information(metadata)}"
        system_prompt = f"""
        **角色扮演开始，你将扮演{self.character_name}。**
        **不要脱离角色。从现在开始，你就是{self.character_name}。**
        以下是{self.character_name}的基本信息：
        
        {dumped_data}
        
        **你的角色是{self.character_name}。**
        **你将使用{self.character_name}的说话风格和行为方式进行对话。**
        **不要脱离角色设定，注意始终保持角色扮演状态。    **
        """
        return system_prompt

    def _build_message(self, role: Literal['user', 'assistant', 'system', 'tool'], content: str = "", images: Sequence[Any] = "") -> Message:
        return {
            "role": role,
            "content": content,
            "images": images if images not in [None, ""] else []
        }

    def _add_into_memory(self, message: Message):
        """ 添加消息到记忆 """
        self.ai_memory.append(message)

    def _write_to_stdout(self, content: str | None) -> None:
        """ 输出到控制台 """
        msg = f"\033[1;38;2;255;119;255m{content}\033[0m"
        sys.stdout.write(msg)
        sys.stdout.flush()
            
    def _send(self, usr_message: str, output_to_console: bool = True, *args, **kwargs) -> str:
        self._add_into_memory(self._build_message("user", usr_message))
        response = self.client.chat.completions.create(model=self.model_name, messages=self.ai_memory, stream=self.stream)
        if self.stream:
            all_content: str = ""
            iter_res = track(response, description="[bold magenta]正在生成...") if not output_to_console else response
            for chunk in iter_res:
                char = chunk.choices[0].delta.content # type: ignore
                all_content += char if char is not None else ""
                if output_to_console:
                    self._write_to_stdout(char)
            self._add_into_memory(self._build_message("assistant", all_content))  # type: ignore
            return all_content # type: ignore
        else:
            cont = response.choices[0].message.content # type: ignore
            self._add_into_memory(self._build_message("assistant", cont))  # type: ignore
            return cont # type: ignore

    def send(self, usr_message: str, output_to_console: bool = True, *args, **kwargs) -> str:
        """ 发送消息 """
        return self._send(usr_message, output_to_console, *args, **kwargs)

if __name__ == '__main__':
    session = Session("glm-4-plus", "your_api_key", stream=True)
    # session.load_another_system_prompt(["注意，你只要根据用户的输入和角色信息来扮演角色就可以了！ 回复尽量长，但也不要太长，可以自己发挥但是不能脱离角色设定，尽量不要有重复的句式回复，允许有括号，但是不能续写用户输入，不能脱离角色扮演状态。", "最最重要的一点，不要对用户的输入进行续写噢，再角色扮演中注意到这一点。"])
    resp = session.send("帮我解读卦象可以吗?")
    print(resp)