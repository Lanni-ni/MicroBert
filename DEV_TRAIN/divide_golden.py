import random
import csv

# ========== 配置 ==========
input_csv = "all_sentences_tokens_entities_golden.csv"  # golden文件 (句子级别)
train_output = "golden_train.csv"
dev_output = "golden_dev.csv"

split_ratio = 0.8
random_seed = 42

# ========== 读入所有句子 ==========
sentences = []  # 每个元素是 (tokens list, labels list)

with open(input_csv, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # 跳过header
    for row in reader:
        tokens_line, labels_line = row
        tokens = tokens_line.strip().split()
        labels = labels_line.strip().split()
        if tokens and labels and len(tokens) == len(labels):
            sentences.append((tokens, labels))

print(f"✅ 读入 {len(sentences)} 个句子")

# ========== 随机划分 ==========
random.seed(random_seed)
random.shuffle(sentences)

split_idx = int(len(sentences) * split_ratio)
train_data = sentences[:split_idx]
dev_data = sentences[split_idx:]

print(f"📄 划分结果: {len(train_data)} 句子用于训练，{len(dev_data)} 句子用于验证")

# ========== 保存到 CSV ==========
def save_sentences(sentences, output_file):
    with open(output_file, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Token", "Label"])
        for tokens, labels in sentences:
            for token, label in zip(tokens, labels):
                writer.writerow([token, label])
            writer.writerow(["", ""])  # 句子之间空行分隔

save_sentences(train_data, train_output)
save_sentences(dev_data, dev_output)

print(f"✅ 保存完毕！Train: {train_output}，Dev: {dev_output}")