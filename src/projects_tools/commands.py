import os
import click
from jinja2 import Environment, PackageLoader
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.status import Status
from rich.syntax import Syntax
from rich.table import Table
from rich import print as rprint
from .utils import console, print_section, print_command

# Initialize Jinja2 environment and rich console
env = Environment(
    loader=PackageLoader('projects_tools', 'templates')
)

@click.group()
def cli():
    """Project management tools"""
    pass

@cli.command()
@click.argument('project_name')
@click.option('--backend', is_flag=True, help='Create Python backend project')
@click.option('--frontend', is_flag=True, help='Create frontend project')
@click.option('--frontend_type', 
              type=click.Choice(['vue', 'reactjs'], case_sensitive=False),
              default='reactjs',
              help='Frontend type: vue or reactjs (default: reactjs)')
@click.option('--enable_proxy', is_flag=True, help='Enable proxy server for frontend')
def create(project_name, backend, frontend, frontend_type, enable_proxy):
    """Create a new project with specified components"""
    if not backend and not frontend:
        console.print("[error]✘ 必须指定至少一个组件 (--backend 或 --frontend)", style="error")
        return

    # 项目创建标题
    console.print(Panel(
        f"[success]🚀 创建新项目: [highlight]{project_name}[/]",
        expand=False,
        style="success"
    ))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        # 修改点：使用 progress 的 task 替代 Status
        init_task = progress.add_task("[info]⚙ 初始化项目结构...", total=1)
        os.makedirs(project_name, exist_ok=True)
        progress.update(init_task, description="[success]✅ 项目目录创建完成", completed=1)

        python_package_name = project_name.replace('-', '_')
        
        if backend:
            print_section("Python 后端设置")
            
            backend_table = Table.grid(padding=(0, 2))
            backend_table.add_row("📦 包结构", Syntax(f"{project_name}/src/{project_name}", "bash"))
            backend_table.add_row("📜 元数据", Syntax("version.py / __init__.py / setup.py", "python"))
            backend_table.add_row("🚀 入口点", Syntax("console_scripts", "ini"))
            console.print(backend_table)
            
            # Create Python project structure
            task_id = progress.add_task("Creating Python project structure...", total=None)
            os.makedirs(os.path.join(project_name, "src"), exist_ok=True)
            os.makedirs(os.path.join(project_name, "src", project_name), exist_ok=True)
            progress.update(task_id, completed=True)
            
            # Create version.py
            task_id = progress.add_task("Creating version.py...", total=None)
            with open(os.path.join(project_name, "src", project_name, "version.py"), "w") as f:
                f.write('__version__ = "0.1.0"\n')
            progress.update(task_id, completed=True)

            # Create __init__.py
            task_id = progress.add_task("Creating __init__.py...", total=None)
            with open(os.path.join(project_name, "src", project_name, "__init__.py"), "w") as f:
                f.write('')
            progress.update(task_id, completed=True)
            
            # Render and write setup.py
            task_id = progress.add_task("Creating setup.py...", total=None)
            setup_template = env.get_template('setup.py.jinja2')
            # Replace hyphens with underscores for Python package name            
            setup_content = setup_template.render(project_name=project_name, python_package_name=python_package_name)
            with open(os.path.join(project_name, "setup.py"), "w") as f:
                f.write(setup_content)
            progress.update(task_id, completed=True)
            
        if frontend:
            print_section(f"前端设置 ({frontend_type.upper()})")
            
            frontend_table = Table.grid(padding=(0, 2))
            frontend_table.add_row("🛠️ 构建工具", "Vite")
            frontend_table.add_row("🎨 UI 框架", "Tailwind CSS")
            frontend_table.add_row("📦 依赖管理", "npm")
            console.print(frontend_table)
            
            # Render and write Makefile
            task_id = progress.add_task("Creating Makefile...", total=None)
            makefile_template = env.get_template('Makefile.jinja2')
            makefile_content = makefile_template.render(project_name=project_name, python_package_name=python_package_name)
            with open(os.path.join(project_name, "Makefile"), "w") as f:
                f.write(makefile_content)
            progress.update(task_id, completed=True)
                
            # Execute frontend setup based on type
            from pathlib import Path
            project_path = Path(project_name)
            
            if frontend_type == 'vue':
                from .vue_tasks import create_vue_project                 
                if not create_vue_project(project_name, project_path):
                    return
            else:
                from .react_tasks import create_react_project
                if not create_react_project(project_name, project_path):
                    return
        
        # Render and write deploy.sh
        task_id = progress.add_task("Creating deploy.sh...", total=None)
        deploy_template = env.get_template('deploy.sh.jinja2')
        deploy_content = deploy_template.render(project_name=project_name, python_package_name=python_package_name)
        with open(os.path.join(project_name, "deploy.sh"), "w") as f:
            f.write(deploy_content)
        os.chmod(os.path.join(project_name, "deploy.sh"), 0o755)
        progress.update(task_id, completed=True)
        
        # Create .gitignore
        task_id = progress.add_task("Creating .gitignore...", total=None)
        with open(os.path.join(project_name, ".gitignore"), "w") as f:
            f.write("web/\nlogs/\n__pycache__/\ndist/\nbuild/\npasted/\n")
        progress.update(task_id, completed=True)

        if enable_proxy:
            # Create proxy.py
            task_id = progress.add_task("Creating proxy server...", total=None)
            proxy_template = env.get_template('proxy.py.jinja2')
            proxy_content = proxy_template.render(
                project_name=project_name, 
                frontend=frontend, 
                python_package_name=python_package_name,
                vue=frontend_type == "vue"
            )
            with open(os.path.join(project_name, "src", project_name, "proxy.py"), "w") as f:
                f.write(proxy_content)
            progress.update(task_id, completed=True)
        
        # Render and write README.md
        task_id = progress.add_task("Creating README.md...", total=None)
        readme_template = env.get_template('README.md.jinja2')
        readme_content = readme_template.render(project_name=project_name)
        with open(os.path.join(project_name, "README.md"), "w") as f:
            f.write(readme_content)
        progress.update(task_id, completed=True)
        
    # 部署配置
    print_section("部署配置")
    deploy_table = Table(show_header=False, box=None)
    deploy_table.add_row("📦 打包脚本", Syntax("./deploy.sh", "bash"))
    deploy_table.add_row("🔧 执行权限", "chmod 755 deploy.sh")
    deploy_table.add_row("🚀 发布命令", Syntax("pip install -e .", "bash"))
    console.print(deploy_table)

    # 最终状态
    console.print(Panel(
        f"[success]✨ 项目 [highlight]{project_name}[/] 创建完成！\n"
        "👉 下一步操作建议:\n"
        f"  cd {project_name}\n"
        "  git init\n"
        "  pip install -e .",
        title="创建成功",
        style="success"
    ))