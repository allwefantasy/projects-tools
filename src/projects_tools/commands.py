import os
import click
import subprocess
from jinja2 import Environment, PackageLoader
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

# Initialize Jinja2 environment and rich console
env = Environment(
    loader=PackageLoader('projects_tools', 'templates')
)
console = Console()

@click.group()
def cli():
    """Project management tools"""
    pass

@cli.command()
@click.argument('project_name')
@click.option('--backend', is_flag=True, help='Create Python backend project')
@click.option('--frontend', is_flag=True, help='Create React frontend project')
@click.option('--enable_proxy', is_flag=True, help='Enable proxy server for frontend')
def create(project_name, backend, frontend, enable_proxy):
    """Create a new project with specified components"""
    if not backend and not frontend:
        console.print("[red]Please specify at least one of --backend or --frontend[/red]")
        return

    console.print(Panel(f"[bold blue]Creating new project: {project_name}[/bold blue]"))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        # Create project directory
        progress.add_task("Creating project directory...", total=None)
        os.makedirs(project_name, exist_ok=True)
        
        if backend:
            console.print("\n[bold cyan]Setting up Python backend:[/bold cyan]")
            
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
            setup_content = setup_template.render(project_name=project_name)
            with open(os.path.join(project_name, "setup.py"), "w") as f:
                f.write(setup_content)
            progress.update(task_id, completed=True)
            
        if frontend:
            console.print("\n[bold cyan]Setting up Frontend:[/bold cyan]")
            
            # Render and write Makefile
            task_id = progress.add_task("Creating Makefile...", total=None)
            makefile_template = env.get_template('Makefile.jinja2')
            makefile_content = makefile_template.render(project_name=project_name)
            with open(os.path.join(project_name, "Makefile"), "w") as f:
                f.write(makefile_content)
            progress.update(task_id, completed=True)
                
            # Execute make ts with real-time output
            console.print("\n[bold yellow]Executing make ts (this may take a few minutes)...[/bold yellow]")
            try:
                process = subprocess.Popen(
                    ['make', 'ts'],
                    cwd=project_name,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    bufsize=1,
                    universal_newlines=True
                )
                
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        console.print(output.strip())
                        
                return_code = process.poll()
                if return_code != 0:
                    console.print(f"[red]make ts command failed with return code {return_code}[/red]")
                    
            except Exception as e:
                console.print(f"[red]Error executing make ts: {str(e)}[/red]")
        
        # Render and write deploy.sh
        task_id = progress.add_task("Creating deploy.sh...", total=None)
        deploy_template = env.get_template('deploy.sh.jinja2')
        deploy_content = deploy_template.render(project_name=project_name)
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
            proxy_content = proxy_template.render(project_name=project_name, frontend=frontend)
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
        
    console.print(Panel(f"[bold green]Successfully created project: {project_name}[/bold green]"))