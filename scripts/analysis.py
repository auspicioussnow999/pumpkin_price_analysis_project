import pandas as pd
import os
import json


def perform_analysis(processed_data_path, report_path):
    """
    执行数据分析并生成报告
    """
    # 读取处理后的数据
    df = pd.read_csv(processed_data_path)

    # 执行分析
    analysis_results = {
        "total_records": len(df),
        "cities": df['City'].nunique(),
        "avg_price": round(df['Avg Price'].mean(), 2),
        "min_price": df['Avg Price'].min(),
        "max_price": df['Avg Price'].max(),
        "price_correlation": df[['Low Price', 'High Price', 'Mostly Low']].corr().to_dict()
    }

    # 确保输出目录存在
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    # 保存分析结果
    with open(report_path, 'w') as f:
        json.dump(analysis_results, f, indent=4)

    print(f"分析报告已保存至: {report_path}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_data_path = os.path.join(base_dir, 'data', 'processed_data.csv')
    report_path = os.path.join(base_dir, 'reports', 'analysis_report.json')

    perform_analysis(processed_data_path, report_path)