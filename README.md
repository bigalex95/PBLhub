# � C++ Learning Journey

> **"Mastering modern C++ through hands-on projects"**

Welcome to my C++ learning branch! This is where I build my understanding of modern C++ (C++17/20) through progressively challenging projects, focusing on practical applications and best practices.

---

## 🎯 Learning Objectives

### Core Concepts to Master

- **Modern C++ Features**: Auto, smart pointers, lambdas, ranges
- **Memory Management**: RAII, stack vs heap, memory safety
- **Object-Oriented Programming**: Classes, inheritance, polymorphism
- **Generic Programming**: Templates, STL containers and algorithms
- **Performance**: Optimization techniques, profiling, benchmarking
- **Build Systems**: CMake, package management, testing frameworks

### Real-World Skills

- Writing clean, maintainable C++ code
- Debugging and profiling applications
- Working with external libraries
- Cross-platform development
- Modern development workflows

---

## � Progress Tracker

| Project           | Status     | Concepts Learned                        | Difficulty      |
| ----------------- | ---------- | --------------------------------------- | --------------- |
| 01-hello-cmake    | ⏳ Planned | CMake basics, build systems             | 🟢 Beginner     |
| 02-calculator-cli | ⏳ Planned | I/O, functions, error handling          | 🟢 Beginner     |
| 03-file-manager   | ⏳ Planned | File I/O, filesystem, strings           | 🟡 Intermediate |
| 04-todo-app       | ⏳ Planned | Classes, STL containers, persistence    | 🟡 Intermediate |
| 05-memory-game    | ⏳ Planned | Dynamic memory, pointers, game logic    | 🟡 Intermediate |
| 06-text-editor    | ⏳ Planned | Advanced I/O, data structures           | 🔴 Advanced     |
| 07-http-client    | ⏳ Planned | Networking, external libraries          | 🔴 Advanced     |
| 08-thread-pool    | ⏳ Planned | Concurrency, threading, synchronization | 🔴 Advanced     |
| 09-mini-database  | ⏳ Planned | File formats, indexing, performance     | 🔴 Advanced     |
| 10-game-engine    | ⏳ Planned | Graphics, architecture, optimization    | 🔴 Expert       |

**Progress**: 0/10 projects completed
**Current Focus**: Setting up development environment
**Next Milestone**: Complete first 3 beginner projects

---

## 🛠️ Development Environment

### Required Tools

- **Compiler**: GCC 11+ or Clang 12+ (C++17/20 support)
- **Build System**: CMake 3.20+
- **Package Manager**: vcpkg or Conan
- **IDE/Editor**: VS Code with C++ extensions or CLion
- **Debugger**: GDB or LLDB
- **Version Control**: Git

### Setup Instructions

1. **Install Compiler and Tools**:

   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install build-essential cmake git

   # macOS (with Homebrew)
   brew install cmake gcc

   # Windows (with vcpkg)
   # Follow vcpkg installation guide
   ```

2. **Verify Installation**:

   ```bash
   g++ --version    # Should show GCC 11+
   cmake --version  # Should show CMake 3.20+
   ```

3. **Clone and Setup**:
   ```bash
   git clone https://github.com/bigalex95/PBLhub.git
   cd PBLhub
   git checkout cpp
   ```

---

## 📁 Project Structure

```
cpp/
├── README.md                 # This file
├── projects/                 # All C++ projects
│   ├── 01-hello-cmake/      # Basic CMake project
│   ├── 02-calculator-cli/   # Command-line calculator
│   └── ...                  # More projects
├── resources/               # Learning materials
│   ├── learning-notes.md    # Personal notes and insights
│   ├── useful-links.md      # Helpful resources and references
│   └── code-snippets/       # Reusable code examples
└── tools/                   # Development utilities
    ├── build-all.sh         # Script to build all projects
    └── run-tests.sh         # Script to run all tests
```

---

## � How to Use This Branch

### For Each Project

1. **Navigate to project directory**:

   ```bash
   cd projects/01-hello-cmake
   ```

2. **Read the project README** for specific instructions

3. **Build the project**:

   ```bash
   mkdir build && cd build
   cmake ..
   make
   ```

4. **Run and test** according to project instructions

### Building All Projects

```bash
# From the cpp branch root
./tools/build-all.sh
```

---

## 📚 Learning Resources

### Essential References

- [C++ Reference](https://en.cppreference.com/) - Comprehensive language reference
- [Modern C++ Guidelines](https://github.com/isocpp/CppCoreGuidelines) - Best practices
- [CMake Tutorial](https://cmake.org/cmake/help/latest/guide/tutorial/) - Build system guide

### Recommended Books

- "A Tour of C++" by Bjarne Stroustrup
- "Effective Modern C++" by Scott Meyers
- "C++ Concurrency in Action" by Anthony Williams

### Online Courses

- [Coursera C++ Specialization](https://www.coursera.org/specializations/c-plus-plus)
- [Udemy Modern C++ Courses](https://www.udemy.com/topic/c-plus-plus/)

---

## 🎯 Next Steps

1. **Set up development environment** (if not done)
2. **Start with Project 01**: Hello CMake
3. **Document learning process** in each project README
4. **Update progress tracker** after each completion
5. **Share insights** in learning-notes.md

---

## 🔗 Navigation

- 🏠 [Back to Main Hub](https://github.com/bigalex95/PBLhub)
- 🐍 [Python Branch](https://github.com/bigalex95/PBLhub/tree/python)
- 📋 [Contributing Guidelines](https://github.com/bigalex95/PBLhub/blob/main/CONTRIBUTING.md)

---

**Let's build something amazing with C++! 🚀**
