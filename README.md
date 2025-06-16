# 🎨 ImFont Compressor

**ImFont Compressor** is a simple and efficient tool built with **Python** for compressing TrueType (`.ttf`) or OpenType (`.otf`) font files. It offers multiple encoding methods and output options to generate lightweight font data, ideal for embedding into C/C++ applications.

---

## ✨ Features

- ✅ Compress fonts using various encoding formats:
  - Unsigned 8-bit (`-u8`)
  - Unsigned 32-bit (`-u32`)
  - Base85 (`-base85`)
- 🔧 Optional compression toggle for raw output.
- 📦 Output as either `static` or `non-static` C data.
- 🧾 Export directly to a `.h` header file.
- 📋 Copy compressed data or save it to disk.
- 🖱️ Drag and drop support for font files.
- 🖼️ Lightweight GUI with intuitive controls.
- 🎨 Custom themes for a personalized interface.
- 🐍 **Built with Python** using `Tkinter` for the GUI.

---

## 📥 Downloads

[![GitHub release](https://img.shields.io/github/v/release/ixDarkLorD/ImFontCompressor?include_prereleases)](https://github.com/ixDarkLorD/ImFontCompressor/releases)

You can download the pre-built executable version of ImFont Compressor for easy use without building from source in the Releases section of the repository.

---

## 🚀 Usage

1. Launch the application.
2. Select or drag a `.ttf` or `.otf` font file into the app.
3. Choose your encoding method.
4. (Optional) Enable/disable compression.
5. Choose between static or non-static data.
6. Select output format (`.h` or `.cpp`).
7. Click **Compress** to generate output.

---

## 🧑‍💻Development

<img src="https://img.shields.io/badge/python-3.13%2B-green?logo=python" alt="Python" />

![Platform](https://img.shields.io/badge/platform-Windows-lightgrey?logo=windows)

- Built for Visual Studio Code, with debug and build tasks preconfigured.
- Use the built-in Run and Debug features for development.
- Cross-platform Python app using Tkinter.

### 📦 Option 1: Using VSCode Task Runner

1. Open the project in **Visual Studio Code**.
2. Press `Ctrl+Shift+P` (or `F1`) to open the **Command Palette**.
3. Select **Run Task**.
4. Choose **⚙️ Setup Project** from the list.

### 🐚 Option 2: Manual Setup

```bash
git clone https://github.com/ixDarkLorD/ImFontCompressor.git
cd ImFontCompressor
python setup.py
```

### 💾 **Note:**

> There is also an optional **Build Compressor** task that rebuilds the compressor C++ executable (`binary_to_compressed_c.exe`) from its source code. Use this if you modify the compressor implementation.

---

## 🙏 Credits

[![License](https://img.shields.io/github/license/ixDarkLorD/ImFontCompressor)](https://github.com/ixDarkLorD/ImFontCompressor/blob/main/LICENSE)

The compression logic is inspired by the original ImGui Font Compressor, widely used for embedding fonts in the Dear ImGui ecosystem.
Special thanks to the ImGui team for their contributions and ideas.
