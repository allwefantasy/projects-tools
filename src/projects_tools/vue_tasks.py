import subprocess
from .utils import console, print_section, print_command
from jinja2 import Environment, PackageLoader
from rich.panel import Panel
from rich.table import Table

# Initialize Jinja2 environment and rich console
env = Environment(
    loader=PackageLoader('projects_tools', 'templates')
)

def create_vue_project(project_name, project_path):
    """Create Vue project with Vite"""
    try:
        # 移除 Status 上下文管理器，改用普通打印
        console.print("[info]🛠 配置 Vue 项目...[/]")

        # 生成 Makefile
        console.print("[info]📄 生成 Makefile...[/]")
        makefile_template = env.get_template('Makefile.jinja2')
        makefile_content = makefile_template.render(project_name=project_name, python_package_name=project_name.replace('-', '_'))
        with open(project_path / "Makefile", "w") as f:
            f.write(makefile_content)

        # 安装前端依赖（保持与 react_tasks.py 一致）
        console.print(f"\n[bold yellow]Executing make vue (this may take a few minutes)...[/bold yellow]")
        print_command("npm create vite@latest")
        
        process = subprocess.Popen(
            ['make', 'vue'],
            cwd=project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )

        # 实时输出日志（与 react_tasks.py 保持同步）
        task_log = []
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                cleaned_output = output.strip()
                task_log.append(cleaned_output)
                console.print(cleaned_output)  # 直接输出，不使用 Status

        return_code = process.poll()
        if return_code != 0:
            error_table = Table.grid(padding=(0, 1))
            error_table.add_row("[error]❌ Vue 项目创建失败")
            error_table.add_row(f"退出码: {return_code}")
            error_table.add_row("最近日志:")
            for line in task_log[-3:]:
                error_table.add_row(f"  [dim]{line}[/]")
            console.print(error_table)
            return False

        # 成功提示保持不变
        success_panel = Panel(
            f"[success]✅ Vue 项目初始化完成\n"
            f"📁 目录结构: [highlight]{project_path}/frontend[/]\n"
            "👉 启动开发服务器: [command]cd frontend && npm run dev[/]",
            style="success",
            expand=False
        )
        console.print(success_panel)
        return True
            
    except Exception as e:
        console.print(Panel(
            f"[error]❌ 创建 Vue 项目时发生错误:[/]\n{str(e)}",
            style="error",
            title="严重错误"
        ))
        return False