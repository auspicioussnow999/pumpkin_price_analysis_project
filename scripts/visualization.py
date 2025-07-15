import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

def visualize_data(data_path, figures_dir):
    """
    生成南瓜价格数据的可视化图表
    """
    # 读取处理后的数据
    df = pd.read_csv(data_path)

    # 确保输出目录存在
    os.makedirs(figures_dir, exist_ok=True)

    # 1. 时间序列分析 - 所有城市的平均价格趋势
    plt.figure(figsize=(12, 6))
    # 确保日期列是日期类型
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df['Avg Price'].resample('M').mean().plot()
        plt.title('南瓜平均价格随时间变化')
        plt.ylabel('平均价格')
        plt.xlabel('日期')
        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, 'price_over_time.png'))
        plt.close()
    else:
        print("警告: 缺少日期列，无法生成时间序列图")

    #2 城市平均价格条形图
    plt.figure(figsize=(10, 6))
    if 'City' in df.columns and 'Avg Price' in df.columns:
        city_avg = df.groupby('City')['Avg Price'].mean().sort_values(ascending=False)
        sns.barplot(
            x=city_avg.values,
            y=city_avg.index,
            palette='viridis'
        )
        plt.title('平均南瓜价格按城市排名')
        plt.xlabel('平均价格')
        plt.ylabel('城市')
        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, 'city_avg_price.png'))
        plt.close()

    # 3. 南瓜类型价格分布
    plt.figure(figsize=(10, 6))
    if 'Type' in df.columns and 'Avg Price' in df.columns:
        # 只显示数量最多的前10种类型
        top_types = df['Type'].value_counts().nlargest(10).index
        df_top = df[df['Type'].isin(top_types)]

        sns.boxplot(
            x='Type',
            y='Avg Price',
            data=df_top,
            palette='Set3'
        )
        plt.title('不同类型南瓜的价格分布')
        plt.xlabel('南瓜类型')
        plt.ylabel('平均价格')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, 'type_price_distribution.png'))
        plt.close()
    else:
        print("警告: 缺少类型或平均价格列，无法生成类型分布图")

    # 4. 价格相关性热力图
    plt.figure(figsize=(10, 8))
    if {'Low Price', 'High Price', 'Avg Price'}.issubset(df.columns):
        numeric_cols = ['Low Price', 'High Price', 'Avg Price']
        corr = df[numeric_cols].corr()
        sns.heatmap(
            corr,
            annot=True,
            cmap='coolwarm',
            fmt=".2f",
            linewidths=.5
        )
        plt.title('价格相关性热力图')
        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, 'price_correlation.png'))
        plt.close()
    else:
        print("警告: 缺少价格列，无法生成相关性热力图")

    # 5. 价格分布直方图
    plt.figure(figsize=(10, 6))
    if 'Avg Price' in df.columns:
        sns.histplot(
            df['Avg Price'],
            bins=30,
            kde=True,
            color='skyblue'
        )
        plt.title('南瓜价格分布')
        plt.xlabel('平均价格')
        plt.ylabel('频率')
        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, 'price_distribution.png'))
        plt.close()
    else:
        print("警告: 缺少平均价格列，无法生成价格分布图")

    print(f"可视化图表已保存至: {figures_dir}")


if __name__ == "__main__":
    # 路径设置
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'processed_data.csv')
    figures_dir = os.path.join(base_dir, 'reports', 'figures')

    visualize_data(data_path, figures_dir)