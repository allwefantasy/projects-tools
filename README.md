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

## Electron+Python项目创建工具

使用以下命令创建一个集成Electron和Python的跨平台桌面应用项目：

```bash
projects electron-python 项目名称 [选项]
```

#### 选项

- `--output-dir`: 指定输出目录，默认为当前目录
- `--debug-mode`: 启用调试模式，打包时会开启控制台窗口，方便查看错误信息
- `--author-name`: 设置项目作者姓名（用于打包信息）
- `--author-email`: 设置项目作者邮箱（用于打包信息）

#### 示例

1. 创建基本的Electron+Python项目：
```bash
projects electron-python my-electron-app
```

2. 创建启用调试模式的项目：
```bash
projects electron-python my-electron-app --debug-mode
```

3. 创建包含作者信息的项目：
```bash
projects electron-python my-electron-app --author-name "Your Name" --author-email "your.email@example.com"
```

这将创建一个具有以下特点的项目：

1. Electron前端界面
2. Python后端服务（使用Flask）
3. 进程间通信机制
4. 跨平台打包配置（Windows, macOS, Linux）
5. 健壮的依赖管理和错误处理

### 项目结构

```
项目名称/
├── package.json           # Electron应用配置
├── main.js                # Electron主进程
├── preload.js             # Electron预加载脚本
├── renderer/              # Electron渲染进程文件
│   ├── index.html
│   ├── index.js
│   └── styles.css
├── python/                # Python引擎代码
│   ├── main.py            # Python主入口
│   ├── requirements.txt   # Python依赖
│   ├── main.spec          # PyInstaller打包配置
│   └── src/               # Python源代码
│       └── ...
└── build/                 # 构建输出目录
    ├── python/            # Python打包输出
    └── electron/          # Electron打包输出
```

### 开发与打包

```bash
# 进入项目目录
cd 项目名称

# 安装依赖
npm install
cd python
pip install -r requirements.txt
cd ..

# 运行开发环境
npm start

# 打包 Python 应用
npm run build:python

# 打包 Python 应用（详细模式，显示更多信息）
npm run build:python:verbose

# 打包完整应用
npm run build:all

# 生成特定平台的安装包
npm run build:win    # Windows
npm run build:mac    # macOS
npm run build:linux  # Linux
```

### 常见问题解决

如果在打包或运行时遇到模块导入错误：

1. 确保已正确安装所有依赖：
```bash
cd python
pip install -r requirements.txt
```

2. 尝试使用调试模式重新创建项目：
```bash
projects electron-python 项目名称 --debug-mode
```

3. 查看详细的打包日志：
```bash
npm run build:python:verbose
```

4. 手动编辑 `python/main.spec` 文件，在 `hiddenimports` 列表中添加缺失的模块

### 打包错误解决

如果遇到与 electron-builder 相关的错误：

1. 确保已设置作者信息：
```bash
projects electron-python 项目名称 --author-name "Your Name" --author-email "your.email@example.com"
```

2. 如果出现 "Cannot compute electron version" 错误，检查 package.json 中的版本号是否为固定版本（没有 ^ 或 ~ 符号）

3. 打包前确保已正确安装 electron 和 electron-builder：
```bash
npm install electron@25.0.0 electron-builder@24.0.0 @electron/rebuild --save-dev
```

4. 如果遇到 "@electron/rebuild" 相关错误，可以运行：
```bash
npm run postinstall
```
这将安装所有必要的应用依赖项。