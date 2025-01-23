from rich.console import Console
from rich.rule import Rule
from rich.theme import Theme


# 定义自定义主题
custom_theme = Theme({
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "info": "bold cyan",
    "highlight": "bold magenta",
    "section": "bold blue reverse",
    "command": "bold yellow"
})

console = Console(theme=custom_theme)

def print_section(title: str):
    """打印带样式的章节标题"""
    console.print(Rule(title, style="section"))

def print_command(cmd: str):
    """高亮显示执行的命令"""
    console.print(f"$ [command]{cmd}[/]", style="highlight")
