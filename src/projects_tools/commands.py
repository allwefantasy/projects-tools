import os
from pathlib import Path
import click
from rich.panel import Panel
from rich import print as rprint

from .utils import console, print_section, print_command
from .project_factory import ProjectFactory
from .components import (
    BackendComponent,
    ReactComponent,
    VueComponent,
    CommonFilesComponent,
    ProxyComponent
)
from .electron_python import ElectronPythonApp

@click.group()
def cli():
    """Project management tools"""
    pass

@cli.command()
@click.argument("project_name")
@click.option("--backend", is_flag=True, help="Create Python backend project")
@click.option("--frontend", is_flag=True, help="Create frontend project")
@click.option("--frontend_type", 
              type=click.Choice(["vue", "reactjs"], case_sensitive=False),
              default="reactjs",
              help="Frontend type: vue or reactjs (default: reactjs)")
@click.option("--enable_proxy", is_flag=True, help="Enable proxy server for frontend")
def create(project_name, backend, frontend, frontend_type, enable_proxy):
    """Create a new project with specified components"""
    if not backend and not frontend:
        console.print("[error]✘ 必须指定至少一个组件 (--backend 或 --frontend)", style="error")
        return
    
    # 准备项目选项
    options = {
        "backend": backend,
        "frontend": frontend,
        "frontend_type": frontend_type,
        "enable_proxy": enable_proxy
    }
    
    # 创建项目路径
    project_path = Path(project_name)
    
    # 准备组件列表
    components = []
    
    # 添加公共文件组件
    components.append(CommonFilesComponent(project_path, project_name, options))
    
    # 如果需要后端，添加后端组件
    if backend:
        components.append(BackendComponent(project_path, project_name, options))
    
    # 如果需要前端，添加相应的前端组件
    if frontend:
        if frontend_type.lower() == "vue":
            components.append(VueComponent(project_path, project_name, options))
        else:  # reactjs is default
            components.append(ReactComponent(project_path, project_name, options))
    
    # 如果需要代理服务器，添加代理组件
    if enable_proxy:
        components.append(ProxyComponent(project_path, project_name, options))
    
    # 使用工厂创建项目
    ProjectFactory.create_project(project_name, components)

@cli.command(help="创建Electron+Python项目")
@click.argument("project_name")
@click.option("--output-dir", default=None, help="输出目录，默认为当前目录")
@click.option("--debug-mode", is_flag=True, help="启用调试模式")
@click.option("--author-name", default=None, help="项目作者姓名")
@click.option("--author-email", default=None, help="项目作者邮箱")
def electron_python(project_name, output_dir, debug_mode, author_name, author_email):
    """创建一个新的Electron+Python项目"""
    app = ElectronPythonApp()
    app.create_project(project_name, output_dir, debug_mode, author_name, author_email)
