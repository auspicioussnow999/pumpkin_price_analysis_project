from configuration import *
from utility import save_json, ensure_dir  # ← 添加 ensure_dir
from data_analysis import *
from model import train_and_evaluate
from evaluate import plot_predictions
import sys
# 将 scripts 目录加入系统路径，避免模块找不到
sys.path.insert(0, os.path.dirname(__file__))

from configuration import *
from utility import save_json
from data_analysis import *
from model import train_and_evaluate
from evaluate import plot_predictions

def run_analysis():
    ensure_dir(os.path.dirname(REPORT_PATH))
    df = load_data(PROCESSED_DATA_PATH)

    results = {
        "overview": summarize_data(df),
        "price_statistics": price_statistics(df),
        "price_correlation": price_correlation(df),
        "monthly_price_trend": monthly_price_trend(df)
    }

    if {'City', 'Type', 'Avg Price'}.issubset(df.columns) and len(df) > 100:
        try:
            ml_results = train_and_evaluate(df)
            results["machine_learning"] = ml_results
            plot_predictions(
                ml_results["sample_predictions"]["actual"],
                ml_results["sample_predictions"]["predicted"],
                os.path.join(os.path.dirname(PROCESSED_DATA_PATH), "figures", "price_predictions.png")
            )
        except Exception as e:
            results["machine_learning"] = f"模型训练失败: {str(e)}"
    else:
        results["machine_learning"] = "缺少必要列或数据量不足"

    save_json(results, REPORT_PATH)
    print("分析完成，结果已保存至:", REPORT_PATH)

if __name__ == "__main__":
    run_analysis()