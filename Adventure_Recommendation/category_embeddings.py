from sentence_transformers import SentenceTransformer
import re
import numpy as np
import pandas as pd

category_descriptions = open('./Adventure_Recommendation/Data/category_descriptions.txt').read()
category_descriptions = category_descriptions.split('---')[1:]

def clean_descr(descr):
    return re.sub("[^A-Za-z .,]", "", descr)

categories = []
descriptions = []
for idx in range(0, len(category_descriptions), 2):
    categories.append(category_descriptions[idx].strip())
    descriptions.append(clean_descr(category_descriptions[idx + 1].strip()))

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
description_embeddings = model.encode(descriptions)
description_embeddings_df = pd.DataFrame(description_embeddings, columns = [f'embedding{x+1}' for x in range(description_embeddings.shape[1])])
description_embeddings_df['category'] = pd.Series(categories)
description_embeddings_df.to_csv('./Adventure_Recommendation/Data/category_embedding.csv', index = False)