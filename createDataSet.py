import jsonlines


import os

file_path = 'output.jsonl'

# 检查文件是否存在，然后删除
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"{file_path} 已删除")

data_samples = [] # (question, ground_truth) = data_samples[index]

# 打开JSONL文件
with jsonlines.open('data/fin.jsonl', 'r') as reader:
    # 逐行读取文件
    for obj in reader:
        print(obj['question'])
        # 映射到 ragas 格式
        data_samples.append((obj['question'], obj['reference_answer']))

import psycopg2

# 配置数据库连接参数
db_config = {
    'dbname': 'lobechat',
    'user': '',
    'password': '',
    'host': 'ep-summer-mouse-a1rjqt9z.ap-southeast-1.aws.neon.tech',
    # 'port': ''
}

try:
    # 连接到PostgreSQL数据库
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    dataset_list = []

    for (question, ground_truth) in data_samples:
    # 执行SQL查询 retrieve 结果
        cursor.execute(
            f"""
SELECT 
    messages.id AS message_id,
    messages.content AS message_content,
    message_queries.id AS query_id,
    message_query_chunks.chunk_id,
    chunks.text
FROM 
    messages
JOIN 
    message_queries ON messages.id = message_queries.message_id
JOIN 
    message_query_chunks ON message_queries.id = message_query_chunks.query_id
JOIN 
    chunks ON message_query_chunks.chunk_id = chunks.id
WHERE 
    messages.content = '{question}';
            """
        )
    # 获取所有返回的数据
        results = cursor.fetchall()
        if len(results) < 1:
            continue
        context = []
    # 处理返回的数据
        for row in results:
    # 执行查询 answer
            single_context = row[4]
            # print(row[4])
            context.append(single_context)
        
        # 获取问题
        msg_id = results[0][0]

        cursor = connection.cursor()
        cursor.execute(f"""
                       SELECT 
    messages.id AS message_id,
    messages.content AS message_content
FROM 
    messages
WHERE
    messages.parent_id = '{msg_id}';
    """)
        results = cursor.fetchall()
        # print(results[0][1])
        answer = results[0][1]

        dataset_list.append({
            'question': question,
            'context': context,
            'answer': answer,
            'ground_truth': ground_truth,
        })
except Exception as error:
    print(f"Error: {error}")
finally:
    # 关闭数据库连接
    if cursor:
        cursor.close()
    if connection:
        connection.close()


# 输出到 JSON Lines 文件
with jsonlines.open(file_path, mode='w') as writer:
    for item in dataset_list:
        writer.write(item)