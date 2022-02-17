import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

category_embeddings = pd.read_csv('./Adventure_Recommendation/Data/category_embedding.csv')
pca = PCA(n_components = 2)
embeddings_2d = pca.fit_transform(category_embeddings[[f'embedding{x+1}' for x in range(category_embeddings.shape[1] - 1)]].values)

plt.scatter(x = embeddings_2d[:, 0], y = embeddings_2d[:, 1])
for idx in range(embeddings_2d.shape[0]):
    plt.annotate(category_embeddings['category'].loc[idx], (embeddings_2d[idx, 0], embeddings_2d[idx, 1]))
plt.show()