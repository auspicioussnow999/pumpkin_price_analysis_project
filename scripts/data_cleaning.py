import pandas as pd
import os
from datetime import datetime
import csv


def clean_data(input_path, output_path):
    """
    清洗南瓜价格数据
    从原始数据生成processed_data.csv
    """
    # 1. 检测文件实际的分隔符
    with open(input_path, 'r', newline='', encoding='utf-8') as f:
        sample = f.read(4096)  # 读取文件前4KB
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        print(f"检测到的分隔符: {repr(dialect.delimiter)}")

    # 2. 定义列名
    column_names = [
        'City Name', 'Type', 'Package', 'Variety', 'Sub Variety', 'Grade', 'Date',
        'Low Price', 'High Price', 'Mostly Low', 'Mostly High', 'Origin', 'Origin District',
        'Item Size', 'Color', 'Environment', 'Unit of Sale', 'Quality', 'Condition',
        'Appearance', 'Storage', 'Crop', 'Repack', 'Trans Mode', 'Unnamed1', 'Unnamed2'
    ]

    # 3. 读取数据 - 移除不兼容的low_memory参数
    try:
        df = pd.read_csv(
            input_path,
            sep=dialect.delimiter,  # 使用检测到的分隔符
            header=0,
            names=column_names,
            engine='python',
            on_bad_lines='warn'
        )
    except Exception as e:
        print(f"读取文件出错: {e}")
        # 尝试使用制表符分隔
        print("尝试使用制表符分隔...")
        try:
            df = pd.read_csv(
                input_path,
                sep='\t',
                header=0,
                names=column_names,
                engine='python',
                on_bad_lines='warn'
            )
        except Exception as e2:
            print(f"使用制表符分隔也失败: {e2}")
            # 尝试让Pandas自动检测分隔符
            print("尝试自动检测分隔符...")
            df = pd.read_csv(
                input_path,
                sep=None,
                header=0,
                names=column_names,
                engine='python',
                on_bad_lines='warn'
            )

    # 4. 打印数据信息以便调试
    print("\n数据基本信息:")
    print(f"行数: {len(df)}")
    print(f"列数: {len(df.columns)}")
    print("前5行数据:")
    print(df.head())

    # 5. 选择需要的列
    required_columns = ['Date', 'City Name', 'Type', 'Low Price', 'High Price']
    # 确保只选择存在的列
    available_columns = [col for col in required_columns if col in df.columns]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(f"警告: 以下列不存在: {missing_columns}")

    df = df[available_columns]

    # 6. 重命名列以保持一致性
    if 'City Name' in df.columns:
        df = df.rename(columns={'City Name': 'City'})

    # 7. 转换日期格式
    def convert_date(date_str):
        # 确保日期是字符串类型
        date_str = str(date_str).strip()
        if not date_str:
            return None

        formats = [
            '%Y/%m/%d',  # 2011/5/16
            '%m/%d/%y',  # 9/24/16
            '%m/%d/%Y',  # 9/24/2016
            '%Y-%m-%d',  # 2011-05-16
            '%m-%d-%y',  # 9-24-16
            '%m-%d-%Y'  # 9-24-2016
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        return None

    if 'Date' in df.columns:
        df['Date'] = df['Date'].apply(convert_date)
        df = df.dropna(subset=['Date'])

    # 8. 处理缺失值和异常值
    if 'Low Price' in df.columns and 'High Price' in df.columns:
        df = df.dropna(subset=['Low Price', 'High Price'])
        df = df[(df['Low Price'] > 0) & (df['High Price'] > 0)]
        # 9. 计算平均价格
        df['Avg Price'] = (df['Low Price'] + df['High Price']) / 2
    else:
        print("警告: 缺少价格列，无法计算平均价格")

    # 10. 保存处理后的数据
    df.to_csv(output_path, index=False)
    print(f"\n清洗后的数据已保存至: {output_path}")
    print(f"处理了 {len(df)} 条记录")
    if 'Date' in df.columns:
        print(f"数据时间范围: {df['Date'].min()} 至 {df['Date'].max()}")


if __name__ == "__main__":
    # 路径设置
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, 'data', 'US-pumpkins.csv')
    output_path = os.path.join(base_dir, 'data', 'processed_data.csv')

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        clean_data(input_path, output_path)
    except Exception as e:
        print(f"\n数据处理出错: {str(e)}")
        import traceback

        traceback.print_exc()