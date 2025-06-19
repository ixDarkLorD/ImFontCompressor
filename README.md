# 🎨 ImFont Compressor

[![GitHub release](https://img.shields.io/github/v/release/ixDarkLorD/ImFontCompressor?style=for-the-badge)](https://github.com/ixDarkLorD/ImFontCompressor/releases)
[![License](https://img.shields.io/github/license/ixDarkLorD/ImFontCompressor?style=for-the-badge)](https://github.com/ixDarkLorD/ImFontCompressor/blob/main/LICENSE)

**ImFont Compressor** is a Python-powered tool for optimizing TrueType (`.ttf`) and OpenType (`.otf`) fonts. Generate lightweight font data perfect for embedding in C/C++ applications with multiple encoding options.

![Application Screenshot](https://i.imgur.com/JRDozvU.png)

---

## ✨ Features

### 🔧 Core Functionality

- Multiple encoding formats:
  - `Unsigned 8-bit` (-u8)
  - `Unsigned 32-bit` (-u32)
  - `Base85` (-base85)
- Toggle raw compression
- Output as `static` or `non-static` C data

### 🚀 Workflow

- Drag-and-drop file loading
- One-click export to `.h` header files
- Clipboard support for quick copying
- Themeable interface (light/dark modes)

### 🛠️ Technical

- Cross-platform Python (3.13+) backend
- Tkinter-based GUI
- Pre-built binaries available

---

## 📦 Installation

Download ready-to-use executables from our [Releases page](https://github.com/ixDarkLorD/ImFontCompressor/releases).

## 🖥️ Usage Guide

1. **Launch the application**
2. **Load font file** _(You can Drag & Drop files)_
3. **Configure**:

   - Encoding method
   - Compression toggle
   - Output type (static/non-static)
   - Export to `.h`/`.cpp`

4. **Generate**:
   - Copy to clipboard
   - Save to disk

---

## ⚙️ Development

<div align="center" style="margin: 10px 0"> <img src="https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white" alt="Windows"> <img src="https://img.shields.io/badge/IDE-VSCode-007ACC?logo=visual-studio-code&logoColor=white" alt="VSCode"> </div>

### 📋 Prerequisites

<div class="prereq-grid">

- **Essential**

  - [Python 3.13+](https://www.python.org/downloads/)
  - [VSCode](https://code.visualstudio.com/) (with Python extension)

- **Optional**
  - [C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - [Git](https://git-scm.com/) (for version control)

</div>

### 🚀 Quick Start

#### 1️⃣ Clone & Open

```bash
git clone https://github.com/ixDarkLorD/ImFontCompressor.git
cd ImFontCompressor
code ImFontCompressor
```

#### 2️⃣ Initialize Environment

**Using VSCode Tasks**:

- <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> → `Type Run Task` → `⚙️ Setup`

**Using Terminal**:

```bash
python setup.py --install
```

#### 3️⃣ Start Developing

Once setup is complete:

- <kbd>F5</kbd> to launch debugger
- <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>B</kbd> to build

### 🗳️ Tasks

<details>
<summary><strong>📋 Click to view development tasks</strong></summary>
<div class="task-grid" style="margin-top: 15px;">

| Task                   | Description                                                                                                    | How to Run                                                                                                                   |
| ---------------------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Setup**              | Initial environment configuration                                                                              | **Terminal**: `python setup.py --install`<br>**VSCode**: `Run Task → Setup`                                                  |
| **Build**              | Create standalone executable                                                                                   | **Terminal**: `python utils/build_exe.py`<br>**VSCode**: <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>B</kbd> or `Run Task → Build` |
| **Release**            | Upload latest build to GitHub Releases                                                                         | **Terminal**: `python utils/upload_release.py`<br>**VSCode**: `Run Task → Release`                                           |
| **Build & Release**    | Runs the full pipeline: builds the application and uploads it                                                  | **Terminal**: `python utils/upload_release.py`<br>**VSCode**: `Run Task → Release`                                           |
| **Compile Compressor** | Compile 'binary_to_compressed_c.cpp' into a standalone compressor executable                                   | **Terminal**: `g++ data/binary_to_compressed_c.cpp`<br>**VSCode**: `Run Task → Build Compressor`                             |
| **Force Setup**        | Performs a full environment reset and reinstall. Use this if you encounter setup issues or need a clean slate. | **Terminal**: `g++ data/binary_to_compressed_c.cpp`<br>**VSCode**: `Run Task → Build Compressor`                             |

</div>
</details>

<details>
<summary>🔍 <strong>Keyboard Shortcuts</strong></summary>

- <kbd>F5</kbd>: Start debugging
- <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>B</kbd>: Build executable
- <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>T</kbd>: Build and Upload executable
- <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> → "Run Task": Access all tasks
</details>

<details>
<summary>💡 <strong>Pro Tips</strong></summary>

1. Use `Force Setup task` or `setup.py --force` to completely rebuild virtual environment
2. Install these VSCode extensions for better experience:
   - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
   - [C++](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools)
3. Set `GITHUB_TOKEN` environment variable for release tasks
4. Check `.vscode/tasks.json` for advanced task configurations
</details>

---

## 🤝 Contributing

- We welcome contributions! Please see our Contribution Guidelines for details.

---

## 📜 License

- This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Inspired by the original Dear ImGui font compressor
- Python/Tkinter community for GUI components
