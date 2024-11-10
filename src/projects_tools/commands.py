def main():
    print("Welcome to Projects Tools!")

if __name__ == "__main__":
    main()
import os
import click
import shutil

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
            
        # Copy setup.py template
        setup_template = os.path.join(os.path.dirname(__file__), "templates", "setup.py")
        with open(setup_template, "r") as f:
            setup_content = f.read().replace("williamtoolbox", project_name)
        with open(os.path.join(project_name, "setup.py"), "w") as f:
            f.write(setup_content)
            
    if frontend:
        # Create Makefile for frontend setup
        makefile_template = os.path.join(os.path.dirname(__file__), "templates", "Makefile")
        shutil.copy(makefile_template, os.path.join(project_name, "Makefile"))
        
    # Copy deploy.sh
    deploy_template = os.path.join(os.path.dirname(__file__), "templates", "deploy.sh")
    shutil.copy(deploy_template, os.path.join(project_name, "deploy.sh"))
    os.chmod(os.path.join(project_name, "deploy.sh"), 0o755)
    
    # Create .gitignore
    with open(os.path.join(project_name, ".gitignore"), "w") as f:
        f.write("web/\nlogs/\n__pycache__/\ndist/\nbuild/\npasted/\n")
        
    click.echo(f"Created project {project_name}")