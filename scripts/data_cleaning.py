import pandas as pd
import os


def clean_data(input_path, output_path):
    """
    清洗南瓜价格数据
    从原始数据生成processed_data.csv
    """
    # 读取原始数据
    df = pd.read_csv(input_path)

    # 示例清洗步骤（根据实际数据调整）：
    # 1. 选择需要的列
    df = df[['Date', 'City', 'Type', 'Low Price', 'High Price', 'Mostly Low']]

    # 2. 处理缺失值
    df = df.dropna()

    # 3. 计算平均价格
    df['Avg Price'] = (df['Low Price'] + df['High Price']) / 2

    # 4. 保存处理后的数据
    df.to_csv(output_path, index=False)
    print(f"清洗后的数据已保存至: {output_path}")


if __name__ == "__main__":
    # 路径设置
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, 'data', 'US-pumpkins.csv')
    output_path = os.path.join(base_dir, 'data', 'processed_data.csv')

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    clean_data(input_path, output_path)