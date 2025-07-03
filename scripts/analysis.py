import pandas as pd
import numpy as np
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from datetime import datetime


def perform_analysis(data_path, report_path):
    """
    分析南瓜价格数据并生成报告
    包含统计摘要、价格相关性、时间趋势分析和机器学习模型
    """
    # 读取处理后的数据
    df = pd.read_csv(data_path)

    # 确保报告目录存在
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    # 1. 数据概览
    analysis_results = {
        "overview": {
            "total_records": len(df),
            "start_date": str(df['Date'].min()) if 'Date' in df.columns else "N/A",
            "end_date": str(df['Date'].max()) if 'Date' in df.columns else "N/A",
            "unique_cities": df['City'].nunique() if 'City' in df.columns else "N/A",
            "unique_types": df['Type'].nunique() if 'Type' in df.columns else "N/A"
        },
        "price_statistics": {
            "low_price_mean": df['Low Price'].mean() if 'Low Price' in df.columns else "N/A",
            "high_price_mean": df['High Price'].mean() if 'High Price' in df.columns else "N/A",
            "avg_price_mean": df['Avg Price'].mean() if 'Avg Price' in df.columns else "N/A",
            "avg_price_std": df['Avg Price'].std() if 'Avg Price' in df.columns else "N/A",
            "avg_price_min": df['Avg Price'].min() if 'Avg Price' in df.columns else "N/A",
            "avg_price_max": df['Avg Price'].max() if 'Avg Price' in df.columns else "N/A"
        }
    }

    # 2. 价格相关性分析
    if {'Low Price', 'High Price', 'Avg Price'}.issubset(df.columns):
        price_corr = df[['Low Price', 'High Price', 'Avg Price']].corr().to_dict()
        analysis_results["price_correlation"] = price_corr
    else:
        analysis_results["price_correlation"] = "缺少价格列"

    # 3. 时间趋势分析
    if 'Date' in df.columns and 'Avg Price' in df.columns:
        # 转换日期列为datetime类型
        df['Date'] = pd.to_datetime(df['Date'])

        # 按月度分析价格趋势
        monthly_avg = df.set_index('Date').resample('M')['Avg Price'].mean()
        monthly_trend = {
            "months": monthly_avg.index.strftime('%Y-%m').tolist(),
            "prices": monthly_avg.values.tolist()
        }
        analysis_results["monthly_price_trend"] = monthly_trend
    else:
        analysis_results["monthly_price_trend"] = "缺少日期或价格列"

    # 4. 添加机器学习模型（线性回归）
    if {'Date', 'City', 'Type', 'Avg Price'}.issubset(df.columns) and len(df) > 100:
        try:
            # 准备数据
            df_ml = df.copy()

            # 从日期中提取月份作为特征
            df_ml['Month'] = pd.to_datetime(df_ml['Date']).dt.month

            # 特征和目标变量
            X = df_ml[['City', 'Type', 'Month']]
            y = df_ml['Avg Price']

            # 分割数据集
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # 创建预处理管道
            preprocessor = ColumnTransformer(
                transformers=[
                    ('cat', OneHotEncoder(handle_unknown='ignore'), ['City', 'Type'])
                ],
                remainder='passthrough'
            )

            # 创建模型管道
            model = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('regressor', LinearRegression())
            ])

            # 训练模型
            model.fit(X_train, y_train)

            # 预测和评估
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            # 存储模型结果
            analysis_results["machine_learning"] = {
                "model_type": "线性回归",
                "features": ["城市", "南瓜类型", "月份"],
                "target": "平均价格",
                "test_size": len(X_test),
                "mean_squared_error": mse,
                "r2_score": r2,
                "sample_predictions": {
                    "actual": y_test.iloc[:5].tolist(),
                    "predicted": y_pred[:5].tolist()
                }
            }

            # 可视化预测结果
            plt.figure(figsize=(10, 6))
            plt.scatter(y_test, y_pred, alpha=0.5)
            plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
            plt.xlabel('实际价格')
            plt.ylabel('预测价格')
            plt.title('实际价格 vs 预测价格')

            # 保存可视化
            fig_dir = os.path.join(os.path.dirname(report_path), 'figures')
            os.makedirs(fig_dir, exist_ok=True)
            plt.savefig(os.path.join(fig_dir, 'price_predictions.png'))
            plt.close()

        except Exception as e:
            analysis_results["machine_learning"] = f"模型训练失败: {str(e)}"
    else:
        analysis_results["machine_learning"] = "缺少必要列或数据量不足"

    # 5. 保存分析报告
    with open(report_path, 'w') as f:
        json.dump(analysis_results, f, indent=4)

    print(f"分析报告已保存至: {report_path}")
    return analysis_results


if __name__ == "__main__":
    # 路径设置
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_data_path = os.path.join(base_dir, 'data', 'processed_data.csv')
    report_path = os.path.join(base_dir, 'reports', 'analysis_report.json')

    # 执行分析
    analysis_results = perform_analysis(processed_data_path, report_path)

    # 打印机器学习结果摘要
    if "machine_learning" in analysis_results and isinstance(analysis_results["machine_learning"], dict):
        ml = analysis_results["machine_learning"]
        print("\n机器学习模型结果:")
        print(f"模型类型: {ml['model_type']}")
        print(f"特征: {', '.join(ml['features'])}")
        print(f"目标: {ml['target']}")
        print(f"测试集大小: {ml['test_size']}")
        print(f"均方误差(MSE): {ml['mean_squared_error']:.2f}")
        print(f"R²分数: {ml['r2_score']:.4f}")
        print("\n样本预测:")
        for i, (actual, predicted) in enumerate(
                zip(ml['sample_predictions']['actual'], ml['sample_predictions']['predicted'])):
            print(f"记录 {i + 1}: 实际={actual:.2f}, 预测={predicted:.2f}, 差异={abs(actual - predicted):.2f}")