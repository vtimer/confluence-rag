# Evaluation RAG vs. Basic Search Engine

This file describes the evaluation of the performance of our RAG chatbot against the basic search engine of Confluence. The scoring system uses a scale of 1 to 3, where 1 is the best score and 3 is the worst score.

## Scoring Criteria

For each query in ``rag.csv`` and ``searchengine.csv``, assign a score of 1, 2 or 3 based on following scoring system. 
Note that lower values indicate better performance. 

After assigning the scores, run:

- ``mann_whitney.py``: to check for statistically significant difference.
- ``vargha_delaney.py``: to calculate the A12 measure.

### Search Engine

The search engine is evaluated based on the position of the relevant result and the associated [Click-Through Rate (CTR)](https://firstpagesage.com/reports/google-click-through-rates-ctrs-by-ranking-position/):

| Position | Score | Criteria                                                                                                                        |
| -------- | ----- | ------------------------------------------------------------------------------------------------------------------------------- |
| 1-2      | 1     | CTR ≈ 60% (User mostly finds what they're looking for without significant effort)                                               |
| 3-7      | 2     | CTR ≈ 35% (Additional clicks or new search queries required; noticeable effort, similar to rephrasing a question for a chatbot) |
| 8+       | 3     | CTR ≈ 5% (Below significance level, as in static testing)                                                                       |

#### Chatbot

The chatbot is evaluated based on the directness and accessibility of the information:

| Score | Criteria                                                       |
| ----- | -------------------------------------------------------------- |
| 1     | Information is directly visible                                |
| 2     | Follow-up question is necessary                                |
| 3     | Multiple follow-up questions required or information not found |

A checklist was created for each question to ensure consistent and unambiguous scoring for the chatbot.
