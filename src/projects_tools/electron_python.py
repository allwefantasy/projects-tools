#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import json
import subprocess
import argparse
import random
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class ElectronPythonApp:
    """处理Electron+Python项目的创建和管理"""
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.templates_dir = os.path.join(self.base_dir, 'templates', 'electron_python')
        # 创建Jinja2环境
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
    
    def create_project(self, project_name, output_dir=None, debug_mode=False, author_name=None, author_email=None):
        """创建一个新的Electron+Python项目
        
        Args:
            project_name: 项目名称
            output_dir: 输出目录，默认为当前目录
            debug_mode: 是否启用调试模式，默认为 False
            author_name: 作者姓名，默认为 "Your Name"
            author_email: 作者邮箱，默认为 "your.email@example.com"
        """
        if output_dir is None:
            output_dir = os.getcwd()
        
        project_dir = os.path.join(output_dir, project_name)
        
        if os.path.exists(project_dir):
            print(f"错误: 目录 {project_dir} 已存在。请选择一个不同的项目名称或删除现有目录。")
            return False
        
        # 创建项目目录结构
        os.makedirs(project_dir)
        os.makedirs(os.path.join(project_dir, 'renderer'))
        os.makedirs(os.path.join(project_dir, 'python', 'src'))
        os.makedirs(os.path.join(project_dir, 'build', 'python'))
        os.makedirs(os.path.join(project_dir, 'build', 'electron'))
        
        # 准备模板变量
        template_vars = {
            'project_name': project_name,
            'python_port': 5000,  # 默认端口
            'debug_console': debug_mode,  # 是否显示控制台
            'author_name': author_name or "Your Name",
            'author_email': author_email or "your.email@example.com"
        }
        
        # 渲染并写入模板文件
        self._render_templates(project_dir, template_vars)
        
        print(f"✅ 成功创建项目: {project_name}")
        print(f"项目位置: {project_dir}")
        print("\n下一步:")
        print(f"  cd {project_name}")
        print("  npm install")
        print("  npm run postinstall  # 安装应用依赖项")
        print("  cd python")
        print("  pip install -r requirements.txt")
        print("  cd ..")
        print("  npm start")
        
        if debug_mode:
            print("\n已启用调试模式，打包后的Python应用将显示控制台窗口，方便查看错误信息。")
        
        return True
    
    def _render_templates(self, project_dir, template_vars):
        """渲染模板文件并写入项目目录"""
        # 主项目目录文件
        self._render_template('package.json.jinja2', os.path.join(project_dir, 'package.json'), template_vars)
        self._render_template('main.js.jinja2', os.path.join(project_dir, 'main.js'), template_vars)
        self._render_template('preload.js.jinja2', os.path.join(project_dir, 'preload.js'), template_vars)
        self._render_template('README.md.jinja2', os.path.join(project_dir, 'README.md'), template_vars)
        self._render_template('gitignore.jinja2', os.path.join(project_dir, '.gitignore'), template_vars)
        
        # 渲染器文件
        self._render_template('index.html.jinja2', os.path.join(project_dir, 'renderer', 'index.html'), template_vars)
        self._render_template('index.js.jinja2', os.path.join(project_dir, 'renderer', 'index.js'), template_vars)
        self._render_template('styles.css.jinja2', os.path.join(project_dir, 'renderer', 'styles.css'), template_vars)
        
        # Python文件
        self._render_template('main.py.jinja2', os.path.join(project_dir, 'python', 'main.py'), template_vars)
        self._render_template('requirements.txt.jinja2', os.path.join(project_dir, 'python', 'requirements.txt'), template_vars)
        self._render_template('main.spec.jinja2', os.path.join(project_dir, 'python', 'main.spec'), template_vars)
    
    def _render_template(self, template_name, output_path, template_vars):
        """渲染单个模板文件"""
        template = self.env.get_template(template_name)
        rendered_content = template.render(**template_vars)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_content)


def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description='创建和管理Electron+Python项目')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 创建新项目命令
    create_parser = subparsers.add_parser('create', help='创建新的Electron+Python项目')
    create_parser.add_argument('project_name', help='项目名称')
    create_parser.add_argument('--output-dir', help='输出目录，默认为当前目录')
    create_parser.add_argument('--debug-mode', action='store_true', help='启用调试模式')
    create_parser.add_argument('--author-name', help='项目作者姓名')
    create_parser.add_argument('--author-email', help='项目作者邮箱')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    if args.command == 'create':
        app = ElectronPythonApp()
        app.create_project(args.project_name, args.output_dir, args.debug_mode,
                          args.author_name, args.author_email)
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 