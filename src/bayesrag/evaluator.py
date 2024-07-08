from datasets import Dataset
from ragas.metrics import context_precision, answer_relevancy
from ragas import evaluate

def evaluate_response(user_query, llm_response, context):
    data_samples = {
        'question': [user_query],
        'answer': [llm_response],
        'contexts': [[context]],
    }
    dataset = Dataset.from_dict(data_samples)
    # if ground_truth:
    #     data_samples['ground_truth'] = [ground_truth]

    # metrics = [context_precision] if ground_truth else [answer_relevancy]
    metrics = [answer_relevancy]
    score = evaluate(dataset, metrics=metrics)
    return score.to_pandas()
