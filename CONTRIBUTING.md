# 🤝 Contributing to PBLhub

This document outlines the standards and guidelines for maintaining the Project-Based Learning Hub repository.

---

## 📋 Repository Management Guidelines

### 🌿 Branch Structure

- **`main`** - Central hub with overview, progress tracking, and navigation
- **Technology branches** (e.g., `cpp`, `python`) - Dedicated learning paths
- **No feature branches** - Direct commits to technology branches for learning projects

### 📁 Project Placement Rules

#### Where to Place New Projects

1. **Determine the technology branch** (cpp, python, etc.)
2. **Switch to the appropriate branch**:
   ```bash
   git checkout [technology-branch]
   ```
3. **Create project in the `projects/` directory**:
   ```
   projects/
   ├── 01-project-name/     # Use 2-digit numbering
   ├── 02-next-project/
   └── 03-advanced-project/
   ```

#### Project Naming Convention

- **Format**: `##-descriptive-name`
- **Examples**: 
  - `01-hello-world`
  - `02-calculator-cli`
  - `03-file-manager`
- **Rules**:
  - Use lowercase with hyphens
  - Start with 2-digit number for ordering
  - Be descriptive but concise
  - Avoid abbreviations when possible

---

## 📝 Documentation Standards

### Required Files for Each Project

#### 1. `README.md` (Mandatory)
Every project must have a comprehensive README with these sections:

```markdown
# Project Name

## 🎯 Problem Statement
Brief description of what real-world problem this project solves.

## 🧠 Concepts Learned
- List of programming concepts
- Technologies used
- Design patterns applied

## 🛠️ Build Instructions
Step-by-step guide to compile/setup the project.

## 🚀 Usage Examples
How to run the project with example commands/inputs.

## 📚 Lessons Learned
Challenges faced and how they were overcome.

## 🔗 Resources
Links to tutorials, documentation, or references used.
```

#### 2. Source Code Organization
```
project-name/
├── README.md
├── src/                 # Main source code
├── include/            # Header files (C++)
├── tests/              # Unit tests
├── docs/               # Additional documentation
├── examples/           # Usage examples
└── build/              # Build artifacts (gitignored)
```

### Documentation Quality Standards

- **Clear and Concise**: Write for your future self
- **Complete**: Include all necessary information to understand and run the project
- **Consistent**: Follow the established template format
- **Updated**: Keep documentation current with code changes

---

## 💻 Commit Message Guidelines

### Format
```
[BRANCH] Type: Brief description

Optional longer description explaining the changes.
```

### Examples
```bash
[cpp] feat: Add basic calculator with arithmetic operations
[python] docs: Update file organizer README with usage examples
[main] update: Refresh progress tracker with completed projects
```

### Types
- **feat**: New project or major feature
- **fix**: Bug fixes or corrections
- **docs**: Documentation updates
- **refactor**: Code improvements without functionality changes
- **test**: Adding or updating tests
- **update**: Progress updates or minor improvements

---

## 🔄 Workflow for Adding New Projects

### Step-by-Step Process

1. **Plan the Project**
   - Define the problem to solve
   - List concepts to learn
   - Estimate complexity level

2. **Set Up Project Structure**
   ```bash
   git checkout [technology-branch]
   mkdir projects/##-project-name
   cd projects/##-project-name
   ```

3. **Create Initial Documentation**
   - Write README.md with problem statement and goals
   - Set up folder structure

4. **Develop the Project**
   - Write code following best practices
   - Test thoroughly
   - Document as you go

5. **Complete Documentation**
   - Update README with lessons learned
   - Add usage examples
   - Include build instructions

6. **Update Progress Tracking**
   - Switch to main branch: `git checkout main`
   - Update progress table in main README.md
   - Commit changes

### Quality Checklist

Before considering a project complete:

- [ ] README.md follows the standard template
- [ ] Code is well-commented and readable
- [ ] Build/run instructions are tested and accurate
- [ ] Project demonstrates the intended learning concepts
- [ ] All files are properly organized
- [ ] Progress tracker is updated

---

## 🎯 Learning Focus Guidelines

### Project Difficulty Progression

- **Beginner (01-03)**: Basic syntax, simple algorithms
- **Intermediate (04-07)**: Data structures, file I/O, APIs
- **Advanced (08-10)**: Complex algorithms, system design, optimization

### Concept Coverage

Ensure each project introduces new concepts while reinforcing previous ones:

- **Don't repeat** the same concepts without adding complexity
- **Build upon** previous projects when possible
- **Document** what's new in each project
- **Connect** concepts across projects

---

## 🚀 Maintenance Guidelines

### Regular Updates

- **Monthly**: Review and update progress tracker
- **Per Project**: Update branch README with new project
- **Quarterly**: Review and improve documentation standards

### Repository Health

- Keep branches focused on their technology
- Maintain consistent formatting across all documentation
- Regularly review and improve project organization
- Archive or refactor outdated projects

---

## ❓ Questions or Suggestions?

For questions about these guidelines or suggestions for improvements:

1. Open an issue in the repository
2. Use the label `documentation` or `process`
3. Provide specific examples when possible

Remember: These guidelines exist to maintain quality and consistency, making the learning journey more effective and the repository more valuable over time.
