import os
import click
import shutil
from jinja2 import Environment, PackageLoader

# Initialize Jinja2 environment
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
@click.option('--frontend', is_flag=True, help='Create React frontend project')
def create(project_name, backend, frontend):
    """Create a new project with specified components"""
    if not backend and not frontend:
        click.echo("Please specify at least one of --backend or --frontend")
        return

    # Create project directory
    os.makedirs(project_name, exist_ok=True)
    
    if backend:
        # Create Python project structure
        os.makedirs(os.path.join(project_name, "src"), exist_ok=True)
        os.makedirs(os.path.join(project_name, "src", project_name), exist_ok=True)
        
        # Create version.py
        with open(os.path.join(project_name, "src", project_name, "version.py"), "w") as f:
            f.write('__version__ = "0.1.0"\n')
            
        # Render and write setup.py
        setup_template = env.get_template('setup.py.jinja2')
        setup_content = setup_template.render(project_name=project_name)
        with open(os.path.join(project_name, "setup.py"), "w") as f:
            f.write(setup_content)
            
    if frontend:
        # Render and write Makefile
        makefile_template = env.get_template('Makefile.jinja2')
        makefile_content = makefile_template.render(project_name=project_name)
        with open(os.path.join(project_name, "Makefile"), "w") as f:
            f.write(makefile_content)
            
        # Execute make ts and capture output
        click.echo("Executing make ts...")
        import subprocess
        try:
            process = subprocess.Popen(['make', 'ts'], 
                                    cwd=project_name,
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            click.echo(stdout.decode())
            if stderr:
                click.echo("Errors:", err=True)
                click.echo(stderr.decode(), err=True)
        except Exception as e:
            click.echo(f"Error executing make ts: {str(e)}", err=True)
        
    # Render and write deploy.sh
    deploy_template = env.get_template('deploy.sh.jinja2')
    deploy_content = deploy_template.render(project_name=project_name)
    with open(os.path.join(project_name, "deploy.sh"), "w") as f:
        f.write(deploy_content)
    os.chmod(os.path.join(project_name, "deploy.sh"), 0o755)
    
    # Create .gitignore
    with open(os.path.join(project_name, ".gitignore"), "w") as f:
        f.write("web/\nlogs/\n__pycache__/\ndist/\nbuild/\npasted/\n")
    
    # Render and write README.md
    readme_template = env.get_template('README.md.jinja2')
    readme_content = readme_template.render(project_name=project_name)
    with open(os.path.join(project_name, "README.md"), "w") as f:
        f.write(readme_content)
        
    click.echo(f"Created project {project_name}")