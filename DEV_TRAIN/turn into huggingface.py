import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer

# ===== 配置 =====
train_file = "final_train.csv"  # 你的训练数据文件
dev_file = "final_dev.csv"      # 你的验证数据文件
tokenizer_name = "bert-base-cased"  # 你选择的预训练模型，可以是 BERT 或 MicroBERT

# ===== 读取 CSV 文件 =====
train_df = pd.read_csv(train_file)
dev_df = pd.read_csv(dev_file)

# ===== 清理数据 =====
def clean_data(df):
    df = df.fillna("")  # 填充 NaN 为 ""，避免出现空值
    df['Token'] = df['Token'].astype(str)  # 确保 Token 列是字符串类型
    df['Label'] = df['Label'].astype(str)  # 确保 Label 列是字符串类型
    return df

train_df = clean_data(train_df)
dev_df = clean_data(dev_df)

# ===== 转换为 Dataset 格式 =====
def convert_to_dataset(df):
    # 将每行 token 和 label 列表转成句子
    sentences = []
    sentence_tokens = []
    sentence_labels = []

    for _, row in df.iterrows():
        sentence_tokens.append(row['Token'])
        sentence_labels.append(row['Label'])

        # 在 CSV 结束或遇到空行就保存当前句子
        if pd.isna(row['Token']) or row['Token'] == "":
            sentences.append((sentence_tokens, sentence_labels))
            sentence_tokens = []
            sentence_labels = []

    # 最后一行句子没有空行
    if sentence_tokens:
        sentences.append((sentence_tokens, sentence_labels))

    # 转换成 Dataset 格式
    return Dataset.from_dict({"tokens": [x[0] for x in sentences], "labels": [x[1] for x in sentences]})

# ===== 转换训练集和验证集 =====
train_dataset = convert_to_dataset(train_df)
dev_dataset = convert_to_dataset(dev_df)

print(f"✅ 转换完成！训练集有 {len(train_dataset)} 条数据，验证集有 {len(dev_dataset)} 条数据")

# ===== Tokenizer =====
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

# ===== Tokenize 数据 =====
def tokenize_function(examples):
    return tokenizer(examples["tokens"], padding="max_length", truncation=True, is_split_into_words=True)

train_dataset = train_dataset.map(tokenize_function, batched=True)
dev_dataset = dev_dataset.map(tokenize_function, batched=True)

# ===== 完成，保存为 Dataset 格式 =====
print("✅ Tokenize 完成，数据已准备好！")