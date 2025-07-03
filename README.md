# pumpkin_price_analysis_project


## 项目概述
分析美国南瓜市场价格趋势和影响因素

## 使用说明
1. 安装依赖：`pip install -r requirements.txt`
2. 数据清洗：`python scripts/data_cleaning.py`
3. 数据分析：`python scripts/analysis.py`
4. 生成可视化：`python scripts/visualization.py`

## 生成的文件
- `data/processed_data.csv`：清洗后的数据
- `reports/analysis_report.json`：分析结果
- `reports/figures/price_trend.png`：价格趋势图
- `reports/figures/city_comparison.png`：城市价格比较

# 南瓜价格分析项目
## 项目概述
该项目旨在分析美国不同地区的南瓜价格数据，探索价格趋势、影响因素，并建立预测模型。项目包括数据清洗、可视化、分析和建模等步骤。
## 项目结构
```
pumpkin_price_analysis_project/
├── data/                   # 数据目录
│   ├── raw/                # 原始数据
│   └── processed/          # 处理后的数据
├── notebooks/              # Jupyter Notebooks
├── reports/                # 分析报告
│   ├── figures/            # 可视化图表
│   └── analysis_report.json# 分析结果
├── scripts/                # 数据处理和分析脚本
│   ├── data_cleaning.py    # 数据清洗脚本
│   ├── visualization.py    # 可视化脚本
│   └── analysis.py         # 分析脚本
├── .gitignore              # Git忽略文件
├── requirements.txt        # 依赖库列表
└── README.md               # 项目说明
```
## 安装指南
1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/pumpkin_price_analysis_project.git
   cd pumpkin_price_analysis_project
   ```
2. 创建虚拟环境（推荐）：
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/MacOS
   venv\Scripts\activate      # Windows
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
## 使用说明
### 数据准备
将原始数据 `US-pumpkins.csv` 放入 `data/raw/` 目录。
### 运行脚本
1. **数据清洗**：
   ```bash
   python scripts/data_cleaning.py
   ```
   该脚本将清洗原始数据并生成处理后的数据到 `data/processed/processed_data.csv`。
2. **数据可视化**：
   ```bash
   python scripts/visualization.py
   ```
   该脚本将生成多种可视化图表并保存到 `reports/figures/`。
3. **数据分析与建模**：
   ```bash
   python scripts/analysis.py
   ```
   该脚本将执行数据分析并生成报告 `reports/analysis_report.json`。
### 使用Notebooks
在 `notebooks/` 目录中提供了探索性分析和建模的Jupyter Notebook。
## 贡献
欢迎贡献！请通过提交Pull Request来提出改进建议。
## 许可证
本项目采用 [MIT 许可证](LICENSE)。
