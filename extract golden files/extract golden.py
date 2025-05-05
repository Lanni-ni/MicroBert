import os
import json
import csv

# ========== 配置路径 ==========
corpora_root = "corpora-master"            # 你的最顶层 corpora 文件夹
meta_path = os.path.join(corpora_root, "meta.json")
output_csv = "all_sentences_tokens_entities_golden.csv"   # 输出 CSV 文件名

# ========== 读取 meta.json 过滤出 golden 文档 ==========
with open(meta_path, "r", encoding="utf-8") as f:
    meta = json.load(f)

golden_doc_ids = {doc_id for doc_id, info in meta.items() if info.get("entities") == "gold"}
print(f"✅ 找到 {len(golden_doc_ids)} 个 golden 文档")

# ========== 开始遍历并提取 ==========
sentences = []     # 保存每句的 tokens
sentence_labels = []  # 保存每句的 labels
tokens = []
entities = []

def clean_entity(entity):
    if entity == "O":
        return "O"
    if entity.startswith("("):
        entity = entity[1:]
    if ")" in entity:
        entity = entity.split(")")[0]
    return entity

for dirpath, dirnames, filenames in os.walk(corpora_root):
    for filename in filenames:
        if filename.endswith(".conllu"):
            full_path = os.path.join(dirpath, filename)
            file_id = os.path.splitext(filename)[0]

            if file_id in golden_doc_ids:
                print(f"📄 正在处理: {full_path}")

                with open(full_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        if line.startswith("#"):
                            if line.startswith("# sent_id"):
                                # 遇到新句子id时，保存上一个句子
                                if tokens:
                                    sentences.append(" ".join(tokens))
                                    sentence_labels.append(" ".join(entities))
                                    tokens = []
                                    entities = []
                            continue

                        parts = line.split("\t")
                        if "-" in parts[0]:
                            continue  # 跳过 multiword token

                        token = parts[1]
                        misc = parts[9]

                        entity = "O"
                        if misc != "_":
                            for item in misc.split("|"):
                                if item.startswith("Entity="):
                                    entity = item.split("=")[1]

                        entity = clean_entity(entity)
                        tokens.append(token)
                        entities.append(entity)

# 最后一行别忘了加进去
if tokens:
    sentences.append(" ".join(tokens))
    sentence_labels.append(" ".join(entities))

# ========== 保存到 CSV ==========
with open(output_csv, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Tokens", "Entities"])
    for toks, ents in zip(sentences, sentence_labels):
        writer.writerow([toks, ents])

print(f"\n✅ 全部完成！提取了 {len(sentences)} 个句子，保存到 {output_csv}")