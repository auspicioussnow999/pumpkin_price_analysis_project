import matplotlib.pyplot as plt
import os
from utility import ensure_dir

def plot_predictions(y_true, y_pred, save_path):
    ensure_dir(os.path.dirname(save_path))
    plt.figure(figsize=(8, 6))
    plt.scatter(y_true, y_pred, alpha=0.5)
    plt.plot([min(y_true), max(y_true)], [min(y_true), max(y_true)], 'r--')
    plt.xlabel("实际价格")
    plt.ylabel("预测价格")
    plt.title("实际 vs 预测价格")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()