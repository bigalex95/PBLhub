# 🔹 PBLhub Branch Workflow Guideline

### **1️⃣ Main Branch (`main`)**

* Purpose: central hub for navigation, progress tracker, and overall roadmap.
* What lives here:

  * `README.md` → roadmap, progress tracker, links to branches.
  * Optional `docs/` → templates, coding conventions, contribution guidelines.
* **Do not** add project source code here.
* **Updates to main**:

  1. When a new project is added in a technology branch:

     * Switch to `main`.
     * Update **progress tracker** and **links to new project folder**.
     * Commit with message: `docs: update progress tracker with <project-name>`.

---

### **2️⃣ Technology Branches (e.g., `cpp`, `python`)**

* Purpose: contain projects for a specific technology.
* Structure per branch:

  ```
  <branch>/
   ├── README.md       # Branch roadmap + project index
   ├── project-01-name/
   │    ├── README.md  # Project details
   │    ├── src/
   │    └── build/     # Optional
   └── project-02-name/
  ```
* **How to add a new project**:

  1. Create a folder: `project-<number>-<name>/`.
  2. Add code, resources, and project README.
  3. Update branch `README.md` with link and short description.
  4. Commit changes: `feat: add <project-name> project`.

---

### **3️⃣ Project Folder Guidelines**

* Each project must have its own `README.md` with:

  1. **Title + Short Description** – what problem it solves.
  2. **Concepts Learned** – programming concepts covered.
  3. **Setup / Run Instructions** – how to build/run project.
  4. **Optional Extended Notes** – deeper explanations, screenshots, diagrams.

---

### **4️⃣ Commit Message Conventions**

* Use clear prefixes for clarity:

  * `feat:` → new project or feature.
  * `docs:` → updates to README, progress tracker.
  * `refactor:` → cleanup, code improvement.
  * `fix:` → bug fixes.
* Example:

  ```
  feat: add C++ calculator project
  docs: update main progress tracker with calculator
  ```

---

### **5️⃣ Updating `main` vs Branches**

* **Code + project README** → always commit in branch.
* **Progress tracker + links** → commit in `main`.
* Never merge branch code into `main`; only manually update documentation.

---

### **6️⃣ Progress Tracker**

* Centralized in `main/README.md`.
* Checklist format:

  ```markdown
  ## Progress Tracker
  ### C++
  - [x] Hello World
  - [ ] Calculator

  ### Python
  - [ ] Guess Number Game
  ```

---

### ✅ Benefits of this Workflow

* Keeps `main` clean and professional.
* Branches are self-contained and can grow independently.
* Clear documentation and progress tracking for all projects.
* Easy navigation for learners and contributors.