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
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            # 生成 Makefile
            task_id = progress.add_task("[info]📄 生成 Makefile...", total=None)
            makefile_template = env.get_template('Makefile.jinja2')
            makefile_content = makefile_template.render(project_name=project_name, python_package_name=project_name.replace('-', '_'))
            with open(project_path / "Makefile", "w") as f:
                f.write(makefile_content)
            progress.update(task_id, completed=True)
            
            # 安装前端依赖
            task_id = progress.add_task("[info]📦 安装前端依赖...", total=None)
            print_command("npm create vite@latest")
            # 执行 make vue 命令
            task_id = progress.add_task("[info]🚀 执行 make vue...", total=None)
            process = subprocess.Popen(
                ['make', 'vue'],
                cwd=project_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True
            )
            
            task_log = []
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    task_log.append(output.strip())
                    progress.update(task_id, description=f"[info]🚀 执行 make vue... {output.strip()}")
                
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