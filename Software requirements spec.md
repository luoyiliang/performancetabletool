
### 版本历史

| 版本  | 日期         | 修改内容   | 作者      |
| --- | ---------- | ------ | ------- |
| 1.0 | 2024-09-22 | 初始版本编写 | Roy Luo |
|     |            |        |         |

---

## 1. 项目简介

`XML to Excel Tool` 是一个基于Python的工具，旨在帮助用户加载和解析特定格式的XML文件，并将其转换为特定格式的Excel文件。该工具为用户提供了直观的图形用户界面（GUI），支持加载多个XML文件，并生成两种不同类型的Excel表格。

### 1.1 目标

- **简化XML文件处理流程**：用户可以选择一个或多个XML文件，并根据其内容生成不同类型的Excel文件。
- **支持用户配置**：在生成Excel文件之前，用户可以配置一些特定的输入选项，以满足不同的业务需求。
- **友好的用户体验**：通过简单易用的图形界面，用户可以快速浏览、选择文件并生成所需的Excel文件。

---

## 2. 功能需求

### 2.1 Load XML

#### 2.1.1 功能描述

该功能允许用户加载一个或多个特定结构的XML文件，并在UI界面上显示文件的关键信息。用户可以通过界面查看加载的文件列表，并识别文件之间的差异。



### 2.1.2 XML文件结构
```
<Margin_Test_Report>
	<GeneralInformation>
		<!-- 文件的基本信息 -->
	</GeneralInformation>
	<TimeEventInformation>
		<!-- TimeEvent相关信息 -->
	</TimeEventInformation>
	<Calibration>
		<!-- 标定数据 -->
	</Calibration>
	<MultiPreprocessingData>
		<!-- 预处理数据 -->
	</MultiPreprocessingData>
	<Channels>
		<!-- 通道信息 -->
	</Channels>
</Margin_Test_Report>

```

#### 2.1.3 功能要求

- **单个文件加载**：用户可以通过文件选择对话框选择一个XML文件进行加载。
- **多个文件加载**：用户可以批量选择多个XML文件，系统应按顺序加载所有文件到内存中。
- **文件信息显示**：
    - 在UI界面上显示已加载XML文件的名称、路径及其主要属性（如文件创建时间、文件大小等）。
    - 提供一个区域显示每个XML文件的关键信息，特别是从 `GeneralInformation` 和 `Calibration` 节点提取的内容。
- **文件列表与差异比较**：
    - 在UI界面上显示已加载的XML文件列表。
    - 如果加载了多个文件，界面应显示文件之间的差异，重点比较 `GeneralInformation` 和 `Calibration` 节点。
    - 差异以表格形式展示，便于用户查看。
- **错误处理**：
    - 当用户加载的XML文件结构不正确时，系统应显示错误提示并记录日志。
    - 支持部分加载：如果多个文件中有部分文件加载失败，程序应继续加载其他文件，并在UI中显示错误文件的状态。

#### 2.1.4 交互流程

1. 用户点击“选择文件”按钮，弹出文件选择对话框。
2. 用户选择一个或多个XML文件，点击“确认”。
3. 系统加载文件，并在UI界面上显示文件列表及其相关信息。
4. 如果有多个文件，系统将提供差异比较功能，允许用户查看文件之间的差异。
5. 加载成功后，用户可以继续进行文件转换操作（如生成Excel文件）。

---

### 2.2 Performance Table Generate

#### 2.2.1 功能描述

该功能将加载的XML文件转换为特定格式的Excel文件。用户需要通过UI界面配置一些输入选项，然后系统根据这些配置将XML文件转换为Excel文件。

**Performance Table** 性能表包括两种类型：

- **Calibration Performance**：用于标定性能结果展示。
- **Misuse/Roughroad Immunity Performance**：用于免疫性能结果展示。

尽管这两种性能表在格式上略有差异，结构上包括以下三个部分：

1. **Title 部分**：
    
    - 描述当前Worksheet表示的性能表类型：
        - Front Calibration Performance
        - Side Calibration Performance
        - Rear Calibration Performance
        - Rollover Calibration Performance
        - Side Misuse Immunity Performance
        - Side Rough Road Immunity Performance
    - 项目名称和Model Year，例如：
        - `P04 24MY`
    - 使用的标定文件名称，例如：
        - `HGWP05______1FHHS04BHHRHHPHHEHX2MH.cal`

2. Sweep parameters部分
	以一个列表的方式展示当前该性能表设定的仿真条件，对于Calibration Performance 和Immunity Performance有较大差异：
	例如Calibration Performance会类似于：
	```
	Sweep Parameters			
          - HighG 0 (X Central) - Gain : 94 to 106 % ( step = 6 )			
          - HighG 0 (X Central) - Offset : -1 to 1 LSB ( step = 1 )			
          - HighG 1 (Y Central) - Gain : 94 to 106 % ( step = 6 )			
          - HighG 1 (Y Central) - Offset : -1 to 1 LSB ( step = 1 )			
          - RSU5 (Side B-Pillar Left RSU) - Gain : 92 to 108 % ( step = 8 )		
          - RSU5 (Side B-Pillar Left RSU) - Offset : -1 to 1 LSB ( step = 1 )	
          - RSU6 (Side B-Pillar Right RSU) - Gain : 92 to 108 % ( step = 8 )	
          - RSU6 (Side B-Pillar Right RSU) - Offset : -1 to 1 LSB ( step = 1 )
	```
	而Immunity Performance 会类似于：
	```
	Sweep Parameters		
          - HighG 0 (X Central) Gain : 50 to 300 % ( step = 1 )		
          - HighG 1 (Y Central) Gain : 50 to 300 % ( step = 1 )		
          - RSU5 (Side B-Pillar Left RSU) Gain : 50 to 300 % ( step = 1 )		
          - RSU6 (Side B-Pillar Right RSU) Gain : 50 to 300 % ( step = 1 )		
	```

3. 性能表部分
包含`File Information Table`和`性能结果表`，`File Name`作为主键连接这两部分。

#### 2.2.2 功能要求

#### 输入配置项
- 用户可以通过界面配置一些输入，如以下内容：
- 支持保存用户的输入配置，方便后续的文件生成。
#### XML文件转换
- 系统将加载的XML文件转换为特定格式的Excel文件。
- 支持批量转换，即用户可以一次性选择多个XML文件并生成多个Excel文件。
- 转换过程中，系统应提供进度条或状态提示，告知用户当前的转换进度。
#### 文件保存
  - 用户可以自行选择保存生成的Excel文件的路径。
  - 默认情况下，生成的文件应保存在与XML文件相同的目录下，并以XML文件名命名。
#### 错误处理
  - 如果XML文件无法转换，系统应提示错误信息，并允许用户重新配置输入项或选择其他文件。
  - 系统应在日志中记录所有转换操作，包括成功与失败的记录。

#### 2.2.3 交互流程

1. 用户点击“Performance Table Generate”按钮，进入配置界面。
2. 用户通过界面选择XML文件，并配置生成Excel文件的相关选项。
3. 用户点击“生成”按钮，系统开始转换XML文件，并在界面上显示转换的进度。
4. 转换完成后，系统弹出提示，告知用户文件生成成功，并提供打开文件的快捷方式。
5. 如果转换失败，系统会显示错误提示，用户可以重新尝试。

---

### 2.3 Calibration Validation Spec Generate

#### 2.3.1 功能描述

该功能与Performance Table Generate类似，允许用户将XML文件转换为另一种特定格式的Excel文件。用户需要通过UI配置输入选项，系统会根据配置将XML文件处理并生成Excel文件。

#### 2.3.2 功能要求

- **输入配置项**：
  - 用户可以通过界面配置一些与校准验证相关的选项（如不同的Excel格式、校准参数等）。
  - 支持保存用户的输入配置，以便后续使用。
- **XML文件转换**：
  - 支持将XML文件转换为特定格式的“Calibration Validation Spec” Excel文件。
  - 批量处理支持：用户可以一次选择多个XML文件进行批量转换。
  - 转换进度和状态应在UI中清晰显示。
- **文件保存**：
  - 用户可以自定义保存路径，默认路径与XML文件相同。
  - 系统应自动命名生成的Excel文件，并允许用户手动修改文件名。
- **错误处理**：
  - 如果XML文件无法转换，系统应显示错误提示，并允许用户重新配置相关选项。
  - 系统应记录所有转换操作的日志，供用户查看。

#### 2.2.3 交互流程

1. 用户点击“Performance Table Generate”按钮，进入配置界面。
2. 用户通过界面选择XML文件，并配置生成Excel文件的相关选项。
3. 用户点击“生成”按钮，系统开始转换XML文件，并在界面上显示转换的进度。
4. 转换完成后，系统弹出提示，告知用户文件生成成功，并提供打开文件的快捷方式。
5. 如果转换失败，系统会显示错误提示，用户可以重新尝试。

---

## 3. 非功能性需求

### 3.1 性能需求
- **内存占用**：在处理大文件时，系统应合理管理内存，避免内存溢出或性能严重下降。

### 3.2 易用性需求

- **界面简洁**：UI设计应简洁直观，用户无需学习即可轻松完成文件加载和转换操作。
- **错误提示清晰**：所有错误提示应明确、具体，帮助用户快速定位问题。

### 3.3 可维护性需求

- **日志记录**：系统应记录所有操作日志，包括文件加载、转换、错误等信息，便于调试和维护。
- **模块化设计**：系统各个功能模块（文件加载、文件转换、日志记录）应独立开发，以便后期维护和扩展。
- 用户控制：系统需要校验用户的名称和当前日期，以限制使用。

---

## 4. 技术要求

- **开发语言**：Python 3.x
- **UI框架**：或 PyQt5
- **XML解析库**：Dom解析
- **Excel生成库**：openpyxl
- **打包工具**：PyInstaller，用于将项目打包成可执行文件。

---

## 5. 约束条件

- **文件格式约束**：系统要求的XML文件必须是特定结构的文件，不符合该结构的文件将无法正常处理。
- **平台支持**：程序应支持Windows。
- **资源限制**：系统在处理超大文件时，性能可能会受到硬件限制（如内存和CPU）。

---

## 6. 验收标准

- **功能验收**：
  - 系统应能够正确加载XML文件，并在界面上显示文件信息。
  - 系统应能够根据用户配置将XML文件成功转换为Excel文件。
  - 系统应能够批量处理多个XML文件，并正确生成多个Excel文件。
- **性能验收**：
  - 文件加载和转换时间应符合性能需求。
  - 系统应在不同平台（Windows、macOS、Linux）上正常运行。
- **用户体验验收**：
  - 界面设计应符合易用性需求，操作流程应简洁、直观。
  - 错误信息应明确，日志记录应完整。


1. 动态表头配置:
   - 使用UI界面中的checkbox来控制表头的显示内容。
   - 表头分为两个主要层级："Time Event Name" 和具体的事件类型（RTTF, Calibration Performance, Margin）。

2. 表头结构:
   - 第一层级: "Time Event Name"（固定）
   - 第二层级: 根据checkbox选择显示RTTF, Calibration Performance, Margin

3. 具体控制逻辑:
   - RTTF部分:
     * checkBox_Rmin 控制 "Min" 列的显示
     * checkBox_Rnom 控制 "Nom" 列的显示
     * checkBox_Rmax 控制 "Max" 列的显示
   - Calibration Performance部分:
     * checkBox_prfmin 控制 "Min" 列的显示
     * checkBox_prfnom 控制 "Nom" 列的显示
     * checkBox_prfmax 控制 "Max" 列的显示
     * checkBox_prfnrate 控制 "NF%" 列的显示
   - Margin部分:
     * comboBox_prf 用于选择显示的具体列（可能是 "Gain" 或其他选项）

4. 特殊控制:
   - checkBox_mrggain: 控制 Margin 下的 "Gain" 列显示

5. 数据结构设计:
   - 设计一个数据结构来存储当前的表头配置
   - 这个结构应该能够反映checkbox的状态和相应的表头显示情况

6. 更新机制:
   - 实现一个更新函数，当checkbox状态改变时调用
   - 这个函数应该更新数据结构并准备新的表头配置

7. 与Dialog集成:
   - 设计一种方法，将配置好的表头传递给用于显示数据的dialog
   - 确保dialog能够根据这个配置正确显示表头和相应的数据列

8. 用户界面响应:
   - 确保UI能够实时反映用户的选择
   - 可能需要一个"应用"或"确认"按钮来最终确认配置

9. 灵活性考虑:
   - 设计应当考虑未来可能的扩展，比如添加新的事件类型或列

10. 验证逻辑:
    - 添加检查以确保至少选择了一个列进行显示
    - 可能需要处理某些列组合的互斥或依赖关系

这个需求梳理提供了一个框架，用于实现通过UI中的checkbox动态配置表头，并将这个配置用于后续的数据显示。实现时，您需要考虑如何在代码中组织这些功能，以及如何有效地管理状态和更新UI。