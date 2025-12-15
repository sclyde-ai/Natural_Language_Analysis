import numpy as np

def high_corr_pairs(corr_matrix, threshold = 1/2):
    """
    相関が大きい組を相関係数行列から取得する
    corr_matrix: 相関係数行列
    threhold: 相関係数の閾値
    """
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    corr_pairs = corr_matrix.where(mask).stack()
    high_corr_pairs = corr_pairs[corr_pairs.abs() > threshold]
    return high_corr_pairs