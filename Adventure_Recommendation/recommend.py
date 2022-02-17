import numpy as np
import pandas as pd
from scipy import spatial

data = pd.read_csv("./Adventure_Recommendation/Data/adventures_processed.csv")

def recommend():
    category_embeddings = pd.read_csv('./Adventure_Recommendation/Data/category_embedding.csv')
    
    user_history = open('./Adventure_Recommendation/Data/user_history.txt').read().split('\n')
    user_history = [x.strip() for x in user_history]
    
    user_history_embeddings = np.zeros((len(user_history), category_embeddings.shape[1] - 1))
    for idx in range(len(user_history)):
        user_history_embeddings[idx, :] = category_embeddings[category_embeddings['category'] == user_history[idx]].iloc[0][[f'embedding{x+1}' for x in range(category_embeddings.shape[1] - 1)]].values
    user_history_embeddings = user_history_embeddings.mean(axis = 0)
    
    all_embeddings = category_embeddings[[f'embedding{x+1}' for x in range(category_embeddings.shape[1] - 1)]].values
    all_categories = category_embeddings['category'].values
    ranking = ((all_embeddings - user_history_embeddings) ** 2).sum(1).argsort()
    return [recommend_activity(all_categories[x]) for x in ranking[:3]]

def recommend_activity(category):
    return data[data['category'] == category.lower()].sort_values(by = 'pref_score', ascending = False).iloc[:5].reset_index(drop = True)