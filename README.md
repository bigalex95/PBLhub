# � Python Learning Journey

> **"Automating the world, one script at a time"**

Welcome to my Python learning branch! This is where I develop practical Python skills through automation projects, data processing tools, and real-world applications that solve everyday problems.

---

## 🎯 Learning Objectives

### Core Concepts to Master

- **Python Fundamentals**: Syntax, data structures, control flow
- **File & Data Processing**: CSV, JSON, XML, file manipulation
- **Web Development**: APIs, web scraping, HTTP requests
- **Automation & Scripting**: Task automation, system administration
- **Data Analysis**: Pandas, NumPy, data visualization
- **Testing & Quality**: Unit testing, code quality, documentation

### Real-World Skills

- Writing clean, Pythonic code
- Building command-line tools and scripts
- Working with APIs and web services
- Data processing and analysis
- Package management and virtual environments
- Debugging and error handling

---

<!-- PROJECT_LIST_START -->

## 📁 Projects

### 01. 01 File Organizer

![Python](https://img.shields.io/badge/Python-✓-green) ![Deps](https://img.shields.io/badge/Dependencies-✓-blue) ![UV](https://img.shields.io/badge/UV-✓-purple)
**Path:** `projects/01-file-organizer/`
**Description:** File Organizer - Project 01 Learning: File I/O, os module, pathlib

```bash
# Run the project
python projects/01-file-organizer/main.py
```

### 02. 02 Password Generator

![Python](https://img.shields.io/badge/Python-✓-green) ![Deps](https://img.shields.io/badge/Dependencies-✓-blue) ![UV](https://img.shields.io/badge/UV-✓-purple)
**Path:** `projects/02-password-generator/`
**Description:** Password Generator - Project 02 Learning: Random, string manipulation, CLI

```bash
# Run the project
python projects/02-password-generator/main.py
```

### 03. 03 Expense Tracker

![Python](https://img.shields.io/badge/Python-✓-green) ![Deps](https://img.shields.io/badge/Dependencies-✓-blue) ![UV](https://img.shields.io/badge/UV-✓-purple)
**Path:** `projects/03-expense-tracker/`
**Description:** Expense Tracker - Project 03 Learning: CSV handling, datetime, data structures

```bash
# Run the project
python projects/03-expense-tracker/main.py
```

### 04. 04 Web Scraper

![Python](https://img.shields.io/badge/Python-✓-green) ![Deps](https://img.shields.io/badge/Dependencies-✓-blue) ![UV](https://img.shields.io/badge/UV-✓-purple)
**Path:** `projects/04-web-scraper/`
**Description:** Web Scraper - Project 04 Learning: Requests, BeautifulSoup, HTML parsing

```bash
# Run the project
python projects/04-web-scraper/main.py
```

### 05. 05 Api Client

![Python](https://img.shields.io/badge/Python-✓-green) ![Deps](https://img.shields.io/badge/Dependencies-✓-blue) ![UV](https://img.shields.io/badge/UV-✓-purple)
**Path:** `projects/05-api-client/`
**Description:** API Client - Project 05 Learning: REST APIs, JSON, error handling

```bash
# Run the project
python projects/05-api-client/main.py
```

### 06. 06 Task Scheduler

![Python](https://img.shields.io/badge/Python-✓-green) ![Deps](https://img.shields.io/badge/Dependencies-✓-blue) ![UV](https://img.shields.io/badge/UV-✓-purple)
**Path:** `projects/06-task-scheduler/`
**Description:** Task Scheduler - Project 06 Learning: Threading, scheduling, system integration

```bash
# Run the project
python projects/06-task-scheduler/main.py
```

### 07. 07 Data Analyzer

![Python](https://img.shields.io/badge/Python-✓-green) ![Deps](https://img.shields.io/badge/Dependencies-✓-blue) ![UV](https://img.shields.io/badge/UV-✓-purple)
**Path:** `projects/07-data-analyzer/`
**Description:** Data Analyzer - Project 07 Learning: Pandas, NumPy, data visualization

```bash
# Run the project
python projects/07-data-analyzer/main.py
```

### 08. 08 Mini Framework

![Python](https://img.shields.io/badge/Python-✓-green) ![Deps](https://img.shields.io/badge/Dependencies-✓-blue) ![UV](https://img.shields.io/badge/UV-✓-purple)
**Path:** `projects/08-mini-framework/`
**Description:** Mini Framework - Project 08 Learning: OOP, decorators, metaclasses

```bash
# Run the project
python projects/08-mini-framework/main.py
```

<!-- PROJECT_LIST_END -->

**Progress**: 0/8 projects completed
**Current Focus**: Setting up Python development environment with virtual environments
**Next Milestone**: Complete first 3 beginner projects

---

## 🛠️ Development Environment

### Required Tools

- **Python**: 3.9+ (preferably 3.11+)
- **Package Manager**: pip, pipenv, or poetry
- **Virtual Environment**: venv or conda
- **IDE/Editor**: VS Code with Python extensions or PyCharm
- **Code Quality**: black, flake8, mypy
- **Testing**: pytest

### Setup Instructions

1. **Install Python and Tools**:

   ```bash
   # Check Python version
   python3 --version  # Should be 3.9+

   # Install pip and venv (if not included)
   sudo apt install python3-pip python3-venv  # Ubuntu/Debian
   brew install python  # macOS
   ```

2. **Set up Virtual Environment**:

   ```bash
   # Create virtual environment
   python3 -m venv venv

   # Activate virtual environment
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install Development Tools**:

   ```bash
   pip install --upgrade pip
   pip install black flake8 pytest requests beautifulsoup4 pandas
   ```

4. **Clone and Setup**:
   ```bash
   git clone https://github.com/bigalex95/PBLhub.git
   cd PBLhub
   git checkout python
   ```

---

## 📁 Project Structure

```
python/
├── README.md                 # This file
├── projects/                 # All Python projects
│   ├── 01-file-organizer/   # Automated file organization
│   ├── 02-password-generator/ # Secure password generator
│   └── ...                  # More projects
├── resources/               # Learning materials
│   ├── learning-notes.md    # Personal notes and insights
│   ├── useful-snippets.py   # Reusable code snippets
│   └── requirements.txt     # Common dependencies
├── tools/                   # Development utilities
│   ├── setup-env.sh         # Environment setup script
│   └── run-tests.sh         # Test runner script
└── venv/                    # Virtual environment (gitignored)
```

---

## � How to Use This Branch

### For Each Project

1. **Activate virtual environment**:

   ```bash
   source venv/bin/activate
   ```

2. **Navigate to project directory**:

   ```bash
   cd projects/01-file-organizer
   ```

3. **Install project dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Read the project README** and follow instructions

5. **Run the project**:
   ```bash
   python main.py
   ```

### Running All Tests

```bash
# From the python branch root
./tools/run-tests.sh
```

---

## 📚 Learning Resources

### Essential References

- [Python Official Documentation](https://docs.python.org/3/) - Comprehensive language reference
- [Real Python](https://realpython.com/) - Practical Python tutorials
- [Python Package Index (PyPI)](https://pypi.org/) - Third-party packages

### Recommended Books

- "Automate the Boring Stuff with Python" by Al Sweigart
- "Python Tricks" by Dan Bader
- "Effective Python" by Brett Slatkin

### Online Resources

- [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- [Codecademy Python Course](https://www.codecademy.com/learn/learn-python-3)
- [Python Cheat Sheet](https://www.pythoncheatsheet.org/)

---

## 🎯 Next Steps

1. **Set up Python development environment** (if not done)
2. **Start with Project 01**: File Organizer
3. **Practice Python fundamentals** through each project
4. **Document learning insights** in learning-notes.md
5. **Update progress tracker** after each completion

---

## 🔗 Navigation

- 🏠 [Back to Main Hub](https://github.com/bigalex95/PBLhub)
- 🔧 [C++ Branch](https://github.com/bigalex95/PBLhub/tree/cpp)
- 📋 [Contributing Guidelines](https://github.com/bigalex95/PBLhub/blob/main/CONTRIBUTING.md)

---

**Let's automate and build with Python! 🐍✨**
