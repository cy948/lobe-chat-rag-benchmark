import argparse
from datasets import Dataset
from dataset_reader import DatasetReader
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_utilization,
    context_recall,
    context_entity_recall,
    answer_similarity,
    answer_correctness,
)

def main():
    command_parser = argparse.ArgumentParser(description='Use -h to print help message')
    command_parser.add_argument('--reader', type=str, required=False, default='jsonl', help='Please select a reader (e.g., jsonl),')
    command_parser.add_argument('--metrics', type=str, required=False, default='context_recall', help='Please select one more metrics (e.g. context_recall)')
    commands = command_parser.parse_args()
    
    # Read then build datase
    data_samples = {}
    if commands.reader == 'jsonl':
        data_samples = DatasetReader().jsonlReader()
    else:
        raise ValueError('Unsupported Reader')
    dataset = Dataset.from_dict(data_samples)
    
    # Read user metrics
    eval_metrics = []
    user_expect_metrics = [item.lstrip() for item in commands.metrics.split(',')]
    for metric in user_expect_metrics:
        if metric == 'context_recall':
            eval_metrics.append(context_recall)
        if metric == 'answer_relevance':
            eval_metrics.append(answer_relevancy)
        if metric == 'context_utilization':
            eval_metrics.append(context_utilization)
        if metric == 'context_entities_recall':
            eval_metrics.append(context_entity_recall)
        if metric == 'answer_semantic_similarity':
            eval_metrics.append(answer_similarity)

    result = evaluate(
        dataset,
        metrics=eval_metrics
    )
    print(result)

if __name__ == '__main__':
    main()