import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def generate_visualizations(processed_data_path, output_dir):
    """
    从处理后的数据生成可视化图表
    并保存到reports/figures目录
    """
    # 读取处理后的数据
    df = pd.read_csv(processed_data_path)

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 1. 价格趋势图
    plt.figure(figsize=(12, 6))
    df['Date'] = pd.to_datetime(df['Date'])
    monthly_avg = df.groupby(df['Date'].dt.to_period('M'))['Avg Price'].mean()
    monthly_avg.plot(kind='line', marker='o')
    plt.title('Monthly Average Pumpkin Price Trend')
    plt.ylabel('Price ($)')
    plt.xlabel('Date')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'price_trend.png'))
    plt.close()

    # 2. 城市价格比较
    plt.figure(figsize=(10, 6))
    city_avg = df.groupby('City')['Avg Price'].mean().sort_values(ascending=False)
    sns.barplot(x=city_avg.values, y=city_avg.index, palette='viridis')
    plt.title('Average Pumpkin Price by City')
    plt.xlabel('Average Price ($)')
    plt.ylabel('City')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'city_comparison.png'))
    plt.close()

    print(f"可视化图表已保存至: {output_dir}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_data_path = os.path.join(base_dir, 'data', 'processed_data.csv')
    output_dir = os.path.join(base_dir, 'reports', 'figures')

    generate_visualizations(processed_data_path, output_dir)