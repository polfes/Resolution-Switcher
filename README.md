# Resolution Switcher 🔄

> RU [Русская версия](./README.ru.md)

> EN [English version](./README.md)

[![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

## 📌 About the project

**Resolution Switcher** is a handy Windows utility that allows you to quickly switch between two preset screen resolutions.

### ✨ Features

- ⚡ **Instant switching** - one click and the resolution changes
- 🎨 **High frequency support** - works with frequencies up to 310 Hz and above
- 💾 **Saving settings** - configuration is stored in `%appdata%\ResolutionSwitcher`
- 🎯 **Select from the available modes** - shows only supported resolutions
- 🖥️ **Color interface** - red for important, white for plain text
- 🔄 **Automatic switching** - remembers the active preset

## 🚀 Installation

### Ready executable file

1. Download `ResolutionSwitcher.exe ` from [Releases](https://github.com/polfes/Resolution-Switcher/releases )
2. Run as an administrator
3. At the first launch, select two permissions
4. It's done!

### 🎮 Usage

```bash
git clone https://github.com/polfes/Resolution-Switcher.git
cd ResolutionSwitcher
pip install pywin32
python resolution_switcher.py

============================================================
     Screen Resolution Switcher
============================================================

What do you want to do?
  - Press ENTER to switch resolution
  - Type 'change' to edit configuration
  - Type 'show' to view current presets
  - Type 'exit' to quit

>

ENTER - toggle resolution
change - change settings
show - show current presets
exit - exit
``

### 🛠️ Compilation

```bash
pip install pyinstaller
compile.bat
```

### 💫 Gratitude
If the project helped you, please put an asterisk on GitHub!

### Development
This project was created in 2026 using a neural network as part of conversational programming.
