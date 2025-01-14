# Makefile for Projects Tools

# The Python interpreter to use
PYTHON := python

FRONTEND_DIR = ./frontend

# Help command to display available commands
help:
	@echo "Available commands:"
	@echo "  make ts    - Setup frontend with React + TypeScript + Tailwind"
	@echo "  make help  - Display this help message"

create_project:	
	npx create-react-app frontend --template typescript
	cd $(FRONTEND_DIR) && rm -rf .git

install_dependencies:
	cd $(FRONTEND_DIR) && npm install -D tailwindcss postcss autoprefixer
	cd $(FRONTEND_DIR) && npm install axios react-router-dom
	cd $(FRONTEND_DIR) && npm install --save-dev @types/react-router-dom

init_tailwind:
	cd $(FRONTEND_DIR) && npx tailwindcss init -p

configure:
	@echo "@import 'tailwindcss/base';" | cat - $(FRONTEND_DIR)/src/index.css > temp && mv temp $(FRONTEND_DIR)/src/index.css
	@echo "@import 'tailwindcss/components';" >> $(FRONTEND_DIR)/src/index.css
	@echo "@import 'tailwindcss/utilities';" >> $(FRONTEND_DIR)/src/index.css
	@echo "/** @type {import('tailwindcss').Config} */" > $(FRONTEND_DIR)/tailwind.config.js
	@echo "module.exports = {" >> $(FRONTEND_DIR)/tailwind.config.js
	@echo "  content: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html']," >> $(FRONTEND_DIR)/tailwind.config.js
	@echo "  theme: {" >> $(FRONTEND_DIR)/tailwind.config.js
	@echo "    extend: {}," >> $(FRONTEND_DIR)/tailwind.config.js
	@echo "  }," >> $(FRONTEND_DIR)/tailwind.config.js
	@echo "  plugins: []," >> $(FRONTEND_DIR)/tailwind.config.js
	@echo "}" >> $(FRONTEND_DIR)/tailwind.config.js

ts: create_project install_dependencies init_tailwind configure

release: ## Build and package web assets	
	cd frontend && npm install && npm run build
	tar -czf web.static.tar.gz -C frontend/build .
	rm -rf src/projects_tools/web && mkdir -p src/projects_tools/web	
	mv web.static.tar.gz src/projects_tools/web/	
	cd src/projects_tools/web/ && tar -xzf web.static.tar.gz && rm web.static.tar.gz
	./deploy.sh && pip install -e .