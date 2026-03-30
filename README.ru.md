# Resolution Switcher 🔄

[![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

## 📌 О проекте

**Resolution Switcher** - это удобная утилита для Windows, которая позволяет быстро переключаться между двумя предустановленными разрешениями экрана.

### ✨ Особенности

- ⚡ **Мгновенное переключение** - один клик и разрешение меняется
- 🎨 **Поддержка высоких частот** - работает с частотами до 310 Гц и выше
- 💾 **Сохранение настроек** - конфигурация хранится в `%appdata%\ResolutionSwitcher`
- 🎯 **Выбор из доступных режимов** - показывает только поддерживаемые разрешения
- 🖥️ **Цветной интерфейс** - красный для важного, белый для обычного текста
- 🔄 **Автоматическое переключение** - запоминает активный пресет

## 🚀 Установка

### Готовый исполняемый файл

1. Скачайте `ResolutionSwitcher.exe` из [Releases](https://github.com/polfes/Resolution-Switcher/releases)
2. Запустите от имени администратора
3. При первом запуске выберите два разрешения
4. Готово!

### 🎮 Использование

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

ENTER - переключить разрешение
change - изменить настройки
show - показать текущие пресеты
exit - выход
```

### 🛠️ Компиляция

```bash
pip install pyinstaller
compile.bat
```

###💫 Благодарность
Если проект вам помог, поставьте звездочку на GitHub!

### Разработка
Этот проект создан в 2026 году с помощью нейросети в рамках диалогового программирования.

