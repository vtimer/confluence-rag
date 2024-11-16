import numpy as np
import pandas as pd

TOP_K = 5

# Load the CSV file AFTER FILLING THE COLUMN 'RELEVANCE'
df = pd.read_csv('query_embedding_source_relevance.csv')


def dcg_at_k(relevance_scores):
    print(relevance_scores)
    relevance_scores = np.asfarray(relevance_scores)[:TOP_K]
    if relevance_scores.size:
        return np.sum((2 ** relevance_scores - 1) / np.log2(np.arange(2, relevance_scores.size + 2)))
    else:
        return 0.0


def ndcg_at_k(relevance_scores, number_relevant_sources):
    dcg_max_table = [1] * number_relevant_sources + [0] * (TOP_K - number_relevant_sources)
    if dcg_max_table is None:
        raise ValueError("dcg_max_table should be defined")
    dcg_max = dcg_at_k(dcg_max_table)
    return dcg_at_k(relevance_scores) / dcg_max


# Calculate metrics for each group
metrics = df.groupby(['query', 'embedding', 'complexity_score']).apply(lambda group: pd.Series({
    'precision': group['relevance'].sum() / TOP_K,
    'recall': group['relevance'].sum() / group['number_all_relevant_sources'].iloc[0],
    'NDCG': ndcg_at_k(group['relevance'].tolist(), group['number_all_relevant_sources'].iloc[0]),
    })).reset_index()

metrics['f1'] = 2 * (metrics['precision'] * metrics['recall']) / (metrics['precision'] + metrics['recall'])
metrics['score'] = ((2 / 3) * metrics['f1'] + (1 / 3) * metrics['NDCG']) * metrics['complexity_score']
metrics.to_csv("query_embedding_source_relevance_with_score.csv")
print(metrics)

# Group by 'embedding' and calculate the average of 'score'
average_scores = metrics.groupby('embedding')['score'].mean().reset_index()
# Rename the columns for clarity
average_scores.columns = ['embedding', 'average_score']
# Sort by average score descending
average_scores = average_scores.sort_values(by='average_score', ascending=False)

# Display the average scores
print("\nAverage Scores for Each Embedding:")
print(average_scores)

# Optionally, you can save the results to a new CSV file
average_scores.to_csv('embeddings_average_scores.csv', index=False)