import csv

# ===== 配置 =====
silver_file = "silver_train.csv"  # 你的 silver BIO 文件
golden_train_file = "golden_train.csv"           # 你的 golden 训练集
final_train_output = "final_train.csv"            # 输出最终训练文件
final_dev_output = "final_dev.csv"                # 直接拷贝 golden_dev

# ===== 读入 silver 和 golden_train =====
def read_sentences(file):
    sentences = []
    current_tokens = []
    current_labels = []
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for row in reader:
            token, label = row
            if token == "":
                if current_tokens:
                    sentences.append((current_tokens, current_labels))
                    current_tokens = []
                    current_labels = []
            else:
                current_tokens.append(token)
                current_labels.append(label)
    if current_tokens:
        sentences.append((current_tokens, current_labels))
    return sentences

silver_sentences = read_sentences(silver_file)
golden_train_sentences = read_sentences(golden_train_file)

print(f"✅ Silver 句子数: {len(silver_sentences)}")
print(f"✅ Golden-train 句子数: {len(golden_train_sentences)}")

# ===== 合并 silver + golden_train =====
final_train_sentences = silver_sentences + golden_train_sentences

print(f"📦 最终 Train 句子数: {len(final_train_sentences)}")

# ===== 保存函数 =====
def save_sentences(sentences, output_file):
    with open(output_file, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Token", "Label"])
        for tokens, labels in sentences:
            for token, label in zip(tokens, labels):
                writer.writerow([token, label])
            writer.writerow(["", ""])  # 每句之间空行

save_sentences(final_train_sentences, final_train_output)

# ===== 拷贝 dev =====
import shutil
shutil.copy("golden_dev.csv", final_dev_output)

print(f"✅ 保存完毕！Train: {final_train_output}，Dev: {final_dev_output}")