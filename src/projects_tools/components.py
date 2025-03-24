"""
Project components implementations for backend and frontend projects.
"""
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table

from .project_factory import ProjectComponent, env
from .utils import console, print_section, print_command


class BackendComponent(ProjectComponent):
    """Python backend project component."""
    
    def create(self) -> bool:
        """Create Python backend project structure."""
        print_section("Python 后端设置")
        
        backend_table = Table.grid(padding=(0, 2))
        backend_table.add_row("📦 包结构", f"{self.project_name}/src/{self.project_name}")
        backend_table.add_row("📜 元数据", "version.py / __init__.py / setup.py")
        backend_table.add_row("🚀 入口点", "console_scripts")
        console.print(backend_table)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            # Create Python project structure
            task_id = progress.add_task("Creating Python project structure...", total=None)
            src_dir = self.project_path / "src"
            package_dir = src_dir / self.python_package_name
            
            os.makedirs(src_dir, exist_ok=True)
            os.makedirs(package_dir, exist_ok=True)
            progress.update(task_id, completed=True)
            
            # Create version.py
            task_id = progress.add_task("Creating version.py...", total=None)
            with open(package_dir / "version.py", "w") as f:
                f.write('__version__ = "0.1.0"\n')
            progress.update(task_id, completed=True)

            # Create __init__.py
            task_id = progress.add_task("Creating __init__.py...", total=None)
            with open(package_dir / "__init__.py", "w") as f:
                f.write('')
            progress.update(task_id, completed=True)
            
            # Render and write setup.py
            task_id = progress.add_task("Creating setup.py...", total=None)
            if not self.render_template('setup.py.jinja2', self.project_path / "setup.py"):
                return False
            progress.update(task_id, completed=True)
            
        return True


class FrontendComponent(ProjectComponent):
    """Base class for frontend project components."""
    
    def __init__(self, project_path: Path, project_name: str, options: Dict[str, Any], 
                 framework_type: str):
        """
        Initialize frontend component.
        
        Args:
            project_path: Path to the project directory
            project_name: Name of the project
            options: Additional options for project creation
            framework_type: Frontend framework type ('vue' or 'reactjs')
        """
        super().__init__(project_path, project_name, options)
        self.framework_type = framework_type
    
    def create(self) -> bool:
        """Create frontend project structure - implemented by subclasses."""
        # Create Makefile
        if not self.render_template('Makefile.jinja2', self.project_path / "Makefile"):
            return False
        return True

    def run_make_command(self, command: str) -> bool:
        """
        Run a make command and show real-time output.
        
        Args:
            command: The make command to run
            
        Returns:
            bool: True if command was successful, False otherwise
        """
        try:
            console.print(f"\n[bold yellow]Executing make {command} (this may take a few minutes)...[/bold yellow]")
            process = subprocess.Popen(
                ['make', command],
                cwd=self.project_path,
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
                    cleaned_output = output.strip()
                    task_log.append(cleaned_output)
                    console.print(cleaned_output)
                    
            return_code = process.poll()
            if return_code != 0:
                error_table = Table.grid(padding=(0, 1))
                error_table.add_row(f"[error]❌ {self.framework_type.upper()} 项目创建失败")
                error_table.add_row(f"退出码: {return_code}")
                error_table.add_row("最近日志:")
                for line in task_log[-3:]:
                    error_table.add_row(f"  [dim]{line}[/]")
                console.print(error_table)
                return False
                
            return True
        except Exception as e:
            console.print(f"[error]Error executing make {command}: {str(e)}[/]")
            return False


class ReactComponent(FrontendComponent):
    """React frontend project component."""
    
    def __init__(self, project_path: Path, project_name: str, options: Dict[str, Any]):
        """Initialize React frontend component."""
        super().__init__(project_path, project_name, options, "reactjs")
    
    def create(self) -> bool:
        """Create React frontend project."""
        print_section("前端设置 (REACTJS)")
        
        frontend_table = Table.grid(padding=(0, 2))
        frontend_table.add_row("🛠️ 构建工具", "Vite")
        frontend_table.add_row("🎨 UI 框架", "Tailwind CSS")
        frontend_table.add_row("📦 依赖管理", "npm")
        console.print(frontend_table)
        
        # Create Makefile (from parent class)
        if not super().create():
            return False
        
        # Run make reactjs command
        if not self.run_make_command("reactjs"):
            return False
        
        # Success message
        console.print(Panel(
            f"[success]✅ React 项目初始化完成\n"
            f"📁 目录结构: [highlight]{self.project_path}/frontend[/]\n"
            "👉 启动开发服务器: [command]cd frontend && npm run dev[/]",
            style="success",
            expand=False
        ))
        
        return True


class VueComponent(FrontendComponent):
    """Vue frontend project component."""
    
    def __init__(self, project_path: Path, project_name: str, options: Dict[str, Any]):
        """Initialize Vue frontend component."""
        super().__init__(project_path, project_name, options, "vue")
    
    def create(self) -> bool:
        """Create Vue frontend project."""
        print_section("前端设置 (VUE)")
        
        frontend_table = Table.grid(padding=(0, 2))
        frontend_table.add_row("🛠️ 构建工具", "Vite")
        frontend_table.add_row("🎨 UI 框架", "Tailwind CSS")
        frontend_table.add_row("📦 依赖管理", "npm")
        console.print(frontend_table)
        
        # Create Makefile (from parent class)
        if not super().create():
            return False
        
        # Run make vue command
        if not self.run_make_command("vue"):
            return False
        
        # Success message
        console.print(Panel(
            f"[success]✅ Vue 项目初始化完成\n"
            f"📁 目录结构: [highlight]{self.project_path}/frontend[/]\n"
            "👉 启动开发服务器: [command]cd frontend && npm run dev[/]",
            style="success",
            expand=False
        ))
        
        return True


class CommonFilesComponent(ProjectComponent):
    """Component for creating common project files."""
    
    def create(self) -> bool:
        """Create common project files like .gitignore, README.md, etc."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            # Create deploy.sh
            task_id = progress.add_task("Creating deploy.sh...", total=None)
            if not self.render_template('deploy.sh.jinja2', self.project_path / "deploy.sh"):
                return False
            # Make deploy.sh executable
            os.chmod(self.project_path / "deploy.sh", 0o755)
            progress.update(task_id, completed=True)
            
            # Create .gitignore
            task_id = progress.add_task("Creating .gitignore...", total=None)
            with open(self.project_path / ".gitignore", "w") as f:
                f.write("web/\nlogs/\n__pycache__/\ndist/\nbuild/\npasted/\n")
            progress.update(task_id, completed=True)
            
            # Create README.md
            task_id = progress.add_task("Creating README.md...", total=None)
            if not self.render_template('README.md.jinja2', self.project_path / "README.md"):
                return False
            progress.update(task_id, completed=True)
        
        # 部署配置
        print_section("部署配置")
        deploy_table = Table(show_header=False, box=None)
        deploy_table.add_row("📦 打包脚本", "./deploy.sh")
        deploy_table.add_row("🔧 执行权限", "chmod 755 deploy.sh")
        deploy_table.add_row("🚀 发布命令", "pip install -e .")
        console.print(deploy_table)
        
        return True


class ProxyComponent(ProjectComponent):
    """Component for creating proxy server."""
    
    def create(self) -> bool:
        """Create proxy server for frontend."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task_id = progress.add_task("Creating proxy server...", total=None)
            
            # Determine if frontend is enabled and its type
            frontend = self.options.get('frontend', False)
            frontend_type = self.options.get('frontend_type', 'reactjs')
            
            context = {
                'frontend': frontend,
                'vue': frontend_type == 'vue'
            }
            
            proxy_path = self.project_path / "src" / self.python_package_name / "proxy.py"
            if not self.render_template('proxy.py.jinja2', proxy_path, context):
                return False
                
            progress.update(task_id, completed=True)
        
        return True 