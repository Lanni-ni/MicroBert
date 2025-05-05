import os
import csv

# ========== 配置路径 ==========
corpora_root = "corpora-master"
doc_ids_file = "silver_doc_ids.txt"
output_csv = "all_sentences_tokens_entities_silver.csv"   # 输出的新csv文件

# ========== 读取需要处理的 doc id ==========
with open(doc_ids_file, "r", encoding="utf-8") as f:
    doc_ids = set(line.strip() for line in f if line.strip())

print(f"✅ 找到 {len(doc_ids)} 个需要处理的文档！")

# ========== 开始遍历并提取 ==========
all_sentences = []  # 每个元素是（token_list, entity_list）

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

            if file_id in doc_ids:
                print(f"📄 正在处理: {full_path}")

                current_tokens = []
                current_entities = []

                with open(full_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()

                        if line.startswith("# sent_id"):
                            # 遇到新的句子ID
                            if current_tokens:
                                all_sentences.append((current_tokens, current_entities))
                                current_tokens = []
                                current_entities = []
                            continue

                        if not line or line.startswith("#"):
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
                        current_tokens.append(token)
                        current_entities.append(entity)

                    # 一个文件结束后，把最后一句补进去
                    if current_tokens:
                        all_sentences.append((current_tokens, current_entities))

print(f"\n✅ 全部完成！提取了 {len(all_sentences)} 个句子！")

# ========== 保存到 CSV ==========
# ========== 保存到 CSV ==========
with open(output_csv, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Tokens", "Entities"])  # 写header

    for tokens, entities in all_sentences:
        token_str = " ".join(tokens)        # token用空格连成一句
        entity_str = " ".join(entities)      # label也用空格连成一句
        writer.writerow([token_str, entity_str])  # 用逗号分开两列