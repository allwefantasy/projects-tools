"""
Project factory module for creating different project types.
This module contains the ProjectFactory class that handles creation of different
project types (backend, frontend with different frameworks).
"""
import os
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union

from jinja2 import Environment, PackageLoader
from rich.panel import Panel

from .utils import console, print_section


# Initialize Jinja2 environment
env = Environment(
    loader=PackageLoader('projects_tools', 'templates')
)


class ProjectComponent(ABC):
    """Abstract base class for project components."""
    
    def __init__(self, project_path: Path, project_name: str, options: Dict[str, Any]):
        """
        Initialize the project component.
        
        Args:
            project_path: Path to the project directory
            project_name: Name of the project
            options: Additional options for project creation
        """
        self.project_path = project_path
        self.project_name = project_name
        self.options = options
        self.python_package_name = project_name.replace('-', '_')
    
    @abstractmethod
    def create(self) -> bool:
        """
        Create the project component.
        
        Returns:
            bool: True if creation was successful, False otherwise
        """
        pass
    
    def render_template(self, template_name: str, output_path: Union[str, Path], 
                        context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Render a template and write it to a file.
        
        Args:
            template_name: Name of the template to render
            output_path: Path where the rendered template should be written
            context: Context data for template rendering
            
        Returns:
            bool: True if rendering was successful, False otherwise
        """
        try:
            if context is None:
                context = {}
            
            # Add common template variables if not provided
            context.setdefault('project_name', self.project_name)
            context.setdefault('python_package_name', self.python_package_name)
            
            template = env.get_template(template_name)
            content = template.render(**context)
            
            with open(output_path, 'w') as f:
                f.write(content)
            
            return True
        except Exception as e:
            console.print(f"[error]Error rendering template {template_name}: {str(e)}[/]")
            return False


class ProjectFactory:
    """Factory for creating different project types."""
    
    @staticmethod
    def create_project(project_name: str, components: List[ProjectComponent]) -> bool:
        """
        Create a project with the specified components.
        
        Args:
            project_name: Name of the project
            components: List of project components to create
            
        Returns:
            bool: True if project creation was successful, False otherwise
        """
        console.print(Panel(
            f"[success]🚀 创建新项目: [highlight]{project_name}[/]",
            expand=False,
            style="success"
        ))
        
        project_path = Path(project_name)
        os.makedirs(project_path, exist_ok=True)
        
        for component in components:
            if not component.create():
                return False
        
        console.print(Panel(
            f"[success]✨ 项目 [highlight]{project_name}[/] 创建完成！\n"
            "👉 下一步操作建议:\n"
            f"  cd {project_name}\n"
            "  auto-coder.chat",
            title="创建成功",
            style="success"
        ))
        
        return True 