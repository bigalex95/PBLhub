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

## � Progress Tracker

| Project               | Status     | Concepts Learned                          | Difficulty      |
| --------------------- | ---------- | ----------------------------------------- | --------------- |
| 01-file-organizer     | ⏳ Planned | File I/O, os module, pathlib              | � Beginner      |
| 02-password-generator | ⏳ Planned | Random, string manipulation, CLI          | 🟢 Beginner     |
| 03-expense-tracker    | ⏳ Planned | CSV handling, datetime, data structures   | 🟡 Intermediate |
| 04-web-scraper        | ⏳ Planned | Requests, BeautifulSoup, HTML parsing     | 🟡 Intermediate |
| 05-api-client         | ⏳ Planned | REST APIs, JSON, error handling           | 🟡 Intermediate |
| 06-task-scheduler     | ⏳ Planned | Threading, scheduling, system integration | 🔴 Advanced     |
| 07-data-analyzer      | ⏳ Planned | Pandas, NumPy, data visualization         | 🔴 Advanced     |
| 08-mini-framework     | ⏳ Planned | OOP, decorators, metaclasses              | 🔴 Advanced     |

**Progress**: 0/8 projects completed
**Current Focus**: Setting up Python development environment
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
