# Projects Tools - 项目创建工具

一个用于快速创建Python前后端项目的命令行工具，支持创建Python后端项目和Vue/React前端项目。

## 安装

```bash
pip install projects-tools
```

## 使用

### 创建新项目

```bash
projects-tools create <project_name> [options]
```

#### 选项

- `--backend`: 创建Python后端项目
- `--frontend`: 创建前端项目
- `--frontend_type`: 前端类型，可选 `vue` 或 `reactjs`（默认：reactjs）
- `--enable_proxy`: 启用前端代理服务器

#### 示例

1. 创建包含Python后端和React前端的项目：
```bash
projects-tools create my-project --backend --frontend
```

2. 创建仅包含Vue前端的项目：
```bash
projects-tools create vue-project --frontend --frontend_type=vue
```

3. 创建包含Python后端、Vue前端并启用代理的项目：
```bash
projects-tools create full-project --backend --frontend --frontend_type=vue --enable_proxy
```

### 项目结构

创建的项目将包含以下文件和目录：

```
project_name/
├── src/
│   └── project_name/  # Python包
│       ├── __init__.py
│       ├── version.py
│       └── proxy.py   # 如果启用了代理
├── frontend/          # 前端项目（如果创建了前端）
├── setup.py           # Python项目配置
├── Makefile           # 构建脚本
├── deploy.sh          # 部署脚本
├── README.md          # 项目说明
└── .gitignore         # Git忽略文件
```

### 启动前端项目

```
cd frontend
npm run dev
```

### 启动后端项目

```
make build_static
pip install -e .
<project_name>.serve
```

### 功能特性

- 自动创建Python项目结构
- 支持Vue和React前端项目创建
- 自动生成setup.py配置文件
- 自动生成Makefile用于构建
- 自动生成部署脚本
- 可选的前端代理服务器支持
- 丰富的命令行提示和进度显示

### 依赖管理

- Python后端项目使用setuptools进行依赖管理
- 前端项目使用npm/yarn进行依赖管理

### 构建与发布

项目创建后，可以使用以下命令进行构建和发布：

1. 发布项目：
```bash
make release
```

### 注意事项

- 确保系统中已安装Node.js和npm/yarn
- 创建前端项目时可能需要较长时间
- 使用代理功能时，请确保端口未被占用

### 开发

要贡献或修改本项目，请克隆仓库并安装开发依赖：

```bash
git clone https://github.com/yourusername/projects-tools.git
cd projects-tools
pip install -e .
```

### 许可证

MIT License