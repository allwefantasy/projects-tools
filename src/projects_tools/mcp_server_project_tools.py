from typing import Any, Dict, List
import asyncio
import argparse
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import os
import subprocess
from jinja2 import Environment, PackageLoader
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Initialize Jinja2 environment and rich console
env = Environment(
    loader=PackageLoader('projects_tools', 'templates')
)
console = Console()

class ProjectsCreatorMCP:
    def __init__(self):
        self.server = Server("mcp_server_project_tools")

    async def setup_server(self):
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            return [
                types.Tool(
                    name="create-project",
                    description="Create a new project with specified components",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_name": {"type": "string"},
                            "backend": {"type": "boolean"},
                            "frontend": {"type": "boolean"},
                            "frontend_type": {
                                "type": "string",
                                "enum": ["vue", "reactjs"]
                            },
                            "enable_proxy": {"type": "boolean"}
                        },
                        "required": ["project_name"]
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: Dict[str, Any] | None
        ) -> List[types.TextContent]:
            if not arguments:
                raise ValueError("Missing arguments")

            if name == "create-project":
                project_name = arguments.get("project_name")
                backend = arguments.get("backend", False)
                frontend = arguments.get("frontend", False)
                frontend_type = arguments.get("frontend_type", "reactjs")
                enable_proxy = arguments.get("enable_proxy", False)

                if not backend and not frontend:
                    return [types.TextContent(
                        type="text",
                        text="Please specify at least one of backend or frontend"
                    )]

                console.print(Panel(f"[bold blue]Creating new project: {project_name}[/bold blue]"))

                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    # Create project directory
                    progress.add_task("Creating project directory...", total=None)
                    os.makedirs(project_name, exist_ok=True)
                    python_package_name = project_name.replace('-', '_')
                    
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
                        setup_content = setup_template.render(project_name=project_name, python_package_name=python_package_name)
                        with open(os.path.join(project_name, "setup.py"), "w") as f:
                            f.write(setup_content)
                        progress.update(task_id, completed=True)
                        
                    if frontend:
                        console.print("\n[bold cyan]Setting up Frontend:[/bold cyan]")
                        
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
                                return [types.TextContent(
                                    type="text",
                                    text="Failed to create Vue project"
                                )]
                        else:
                            from .react_tasks import create_react_project
                            if not create_react_project(project_name, project_path):
                                return [types.TextContent(
                                    type="text",
                                    text="Failed to create React project"
                                )]
                    
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
                    
                return [types.TextContent(
                    type="text",
                    text=f"Successfully created project: {project_name}"
                )]

            else:
                raise ValueError(f"Unknown tool: {name}")

    async def run(self):
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp_server_project_tools",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

async def main():
    server = ProjectsCreatorMCP()
    await server.setup_server()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())