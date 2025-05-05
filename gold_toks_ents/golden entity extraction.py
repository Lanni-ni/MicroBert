import os
import csv

# ========== 配置路径 ==========
corpora_root = "corpora-master"         # 你的最顶层 corpora 文件夹
doc_ids_file = "golden_doc_ids.txt"      # 这里可以换成 "golden_doc_ids.txt"
output_csv = "all_tokens_entities_golden.csv"   # 输出的 csv 文件

# ========== 读取需要处理的 doc id ==========
with open(doc_ids_file, "r", encoding="utf-8") as f:
    doc_ids = set(line.strip() for line in f if line.strip())

print(f"✅ 找到 {len(doc_ids)} 个需要处理的文档！")

# ========== 开始遍历并提取 ==========
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
            # 文件名不含扩展名，比如 "1Cor_01"
            file_id = os.path.splitext(filename)[0]

            # 检查是否在 doc id 列表中
            if file_id in doc_ids:
                print(f"📄 正在处理: {full_path}")

                with open(full_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
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
                        tokens.append(token)
                        entities.append(entity)

# ========== 保存到 CSV ==========
with open(output_csv, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Token", "Entity"])
    for token, entity in zip(tokens, entities):
        writer.writerow([token, entity])

print(f"\n✅ 全部完成！提取了 {len(tokens)} 个 token，保存到 {output_csv}")