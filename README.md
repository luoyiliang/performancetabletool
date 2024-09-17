


# XML to Excel Tool

## 项目简介
这是一个基于 Python 的工具，用于解析特定 XML 文件并生成特定格式的 Excel 文件。该工具提供了用户友好的图形界面，使用户能够轻松选择 XML 文件并生成所需的 Excel 报表。该项目设计简洁，适用于需要将 XML 数据批量转换为 Excel 的场景。

## 功能特点

- **XML 文件解析**：支持特定的 XML 文件格式，提取数据。
- **Excel 文件生成**：将解析的 XML 数据导出为 Excel 文件，支持自定义表格格式。
- **用户界面**：提供简易的图形界面，便于用户操作。
- **日志功能**：记录操作日志，方便排查和调试。
- **打包成可执行文件**：可以生成独立的 `.exe` 文件，便于分发和使用。

## Folder Structure

PERFORMANCETABLETOOL/
├─bin   # 存放可执行文件
├─config  # 存放配置文件
├─gui  # 存放图形界面文件
├─models  # 存放模型文件
│  └─__pycache__
├─src  # 存放资源文件
│  ├─assets  # 存放资源文件
│  ├─helper  # 存放帮助文档
│  ├─icons  # 存放图标
│  └─styles  # 存放样式文件
├─tests  # 存放测试文件
└─utils  # 存放工具文件