import jsonlines as jl
import os
from utils import get_env_name


class DatasetReader:
    def __init__(self) -> None:
        self.data_samples = {
            'question': [],
            'contexts': [],
            'ground_truth': [],
            'answer': [],
        }
    def jsonlReader(self):
        READER_JSONL_FILE_PATH = os.environ[get_env_name('reader', 'jsonl', 'file_path')]
        with jl.open(READER_JSONL_FILE_PATH, 'r') as reader:
            for obj in reader:
                self.data_samples['question'].append(obj['question'])
                self.data_samples['contexts'].append(obj['context'])
                self.data_samples['ground_truth'].append(obj['ground_truth'])
                self.data_samples['answer'].append(obj['answer'])
        return self.data_samples

    