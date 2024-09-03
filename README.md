# RAG benchmark

## 运行评测Cli工具

```sh
export export READER_JSONL_FILE_PATH='./data/eval.jsonl'
export OPENAI_API_KEY=
export OPENAI_BASE_URL=
python cli.py --reader=jsonl --metrics=context_recall
```

参数参考：

1. `--reader`读取数据集的Reader，非必选，默认为`jsonl`；

2. `--metrics`评测数据集的指标，非必选，默认为`context_recall`，可选值有：
- `context_recall`
- `answer_relevance`
- `context_utilization`
- `context_entities_recall`
- `answer_semantic_similarity`
> 指标解释见：https://docs.ragas.io/en/latest/concepts/metrics/index.html

## 数据集构建

### 数据结构

- [FinLongEval](https://github.com/valuesimplex/FinLongEval/tree/main)数据集中的数据结构

```python
{
    'question': '问答对中的问题',
    'reference_answer': '问答对中的参考答案',
    'document_name': '回答问题可参考的文档'
}
```

- 评测时所需的数据
> 以单个 sample 为例

```python
{
    'question': '问答对中的问题',
    'context': ['RAG检索器根据问题检索得到的 chunks'],
    'answer': 'LLM 生成的答案',
    'ground_truth': '问答对中的参考答案'
}
```

- RAG生成答案时所需的结构

```python
{
    'question': '问答对中的问题',
    'document_name': '回答问题可供参考的文档'
}
```

### 构建过程

1. 选择部分问答对，并上传其对应文档到 lobechat 知识库中，选中知识库，输入数据集中的问题。此部分用到的文件：
- `fintocsv.py` 将 FinLongEval 数据集转为 csv 格式，方便复制粘贴进 lobechat 的文本框中；

2. 使用 SQL 从数据库中选择对应问题的回复、Retrieve chunks，构建数据集
- `createDataSet.py` 从数据集中读取问题，并从`messages`表中读取问题的`query_id`，从而读取`chunks`；

### 数据集构建的规模扩增问题

1. 问题
- 手动上传文件并分块、指定问题回答的知识库、输入问题的手动操作导致无法扩增；
- 构建数据集时依赖数据库字符串对比功能对同一问题进行匹配，即匹配问题的评测结果和数据集的`ground_truth`。该办法对问题的输入有高要求，必须每个字符都对应，否则数据库可能检索不出对应的历史；

2. 是否存在一个 API 能够：

- 对文件进行RAG，完成上传、分块、向量化，并返回知识库的标识符；
```ts
function UploadFileToRAGPipeline(fileUrl: string[]){
    // some logics
    return {} as {
        knowledgeBaseIdentifiers: string[]
    }
}
```

- 提供一种这样的 completion 方法：
> 以下只是必要的变量，日后可以继续增加

```ts
function Completion(
    knowledgeBaseIdentifier: string, // 知识库的标识符
    question: string,
    ground_truth: string, // 只是为了透传
){
    return {
        // 以下参数应该直接将原来的入参的变量传回
        question,
        ground_truth,
    } as {
        question: string; // 直接读取入参
        ground_truth: string; // 直接读取入参
        answer: string; // Lobe 生成的回复
        contexts: string[]; // Lobe 检索器检索的chunks内容
    }
}
```

## 评测

使用 RAGAS 对生成的数据集进行评测，指标可以在 `evaluate.ipnb` 中进行增减。

