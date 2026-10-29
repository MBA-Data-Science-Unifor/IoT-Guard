import pandas as pd
import numpy as np
import modulefinder


def correlation_groups(corr_matrix: pd.DataFrame, threshold=0.95) -> list[set]:
    """ 
    Agrupa as features conectadas por |p| > threshold usando a matriz completa
    """
    columns = corr_matrix.columns.tolist()
    n = len(columns)

    new_corr_matrix = corr_matrix.fillna(0.0).to_numpy(dtype="float")
    new_corr_matrix = np.maximum(new_corr_matrix, new_corr_matrix.T) # simetriza

    condition = (new_corr_matrix >= threshold) & ~np.eye(n, dtype=bool) # criação de uma matriz bidimensional para identificar  os resultados

    visited, groups = set(), []

    for i in range(n):
        if i in visited:
            continue
        stack, group_idx = [i], set()

        while stack:
            node = stack.pop()
            if node in visited:
                continue
            
            visited.add(node)
            group_idx.add(node)

            for value in range(n):
                if condition[node, value] and value not in visited:
                    stack.append(value)

        groups.append({columns[v] for v in group_idx})
    
    return groups


def choose_columns(group_list: list[dict], importances:dict):
    """ 
    Para cada grupo será escolhido a feature com mais importância
    """
    keep_columns, remove_columns = [], []
    
    for g in group_list:
        if len(g) == 1:
            keep_columns.extend(g)
            continue
        
        best = max(g, key=lambda f: importances.get(f))
        keep_columns.append(best)
        remove_columns.extend(g - {best})
    return keep_columns, remove_columns
