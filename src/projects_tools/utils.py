console = Console(theme=custom_theme)

def print_section(title: str):
    """打印带样式的章节标题"""
    console.print(Rule(title, style="section"))

def print_command(cmd: str):
    """高亮显示执行的命令"""
    console.print(f"$ [command]{cmd}[/]", style="highlight")
