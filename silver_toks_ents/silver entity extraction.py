import os
import csv

# ======= 配置路径 =======
root_folder = "corpora-master"   # 你的最上层目录
output_csv = "all_tokens_entities.csv"  # 输出大表格

tokens = []
entities = []

# ======= 小函数：清理 entity =======
def clean_entity(entity):
    if entity == "O":
        return "O"
    if entity.startswith("("):
        entity = entity[1:]  # 去掉最前面的 (
    if ")" in entity:
        entity = entity.split(")")[0]  # 遇到多个，比如 person)abstract)，取第一个
    return entity

# ======= 遍历所有文件夹 =======
for dirpath, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        if filename.endswith(".conllu"):
            file_path = os.path.join(dirpath, filename)
            print(f"正在处理: {file_path}")

            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue  # 跳过注释和空行

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

                    entity = clean_entity(entity)  # 🛠️ 在这里清理 entity
                    tokens.append(token)
                    entities.append(entity)

# ======= 保存成 CSV =======
with open(output_csv, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Token", "Entity"])
    for token, entity in zip(tokens, entities):
        writer.writerow([token, entity])

print(f"✅ 全部完成！共提取了 {len(tokens)} 个 token，输出文件保存在：{output_csv}")