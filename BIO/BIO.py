import pandas as pd

# 加载数据
train_path = "final_train.csv"
dev_path = "final_dev.csv"

train_df = pd.read_csv(train_path)
dev_df = pd.read_csv(dev_path)

# === 1. 查看原始NER类别 ===
def get_label_set(df):
    return set(label for label in df['Label'].unique() if label != '0' and label != 'O')

print("Train集 NER类别：", get_label_set(train_df))
print("Dev集 NER类别：", get_label_set(dev_df))

# === 2. 转成BIO格式 ===
def convert_to_BIO(df):
    new_tokens = []
    new_labels = []

    last_entity = None

    for idx, row in df.iterrows():
        token = row['Token']
        label = row['Label']

        if pd.isna(label) or label == "0" or label == "O":
            new_tokens.append(token)
            new_labels.append("O")
            last_entity = None
        else:
            entity_type = label.split("-")[0]  # 只取类别前缀，比如person-Basil_of_Caesarea => person
            if last_entity != entity_type:
                new_labels.append("B-" + entity_type)
            else:
                new_labels.append("I-" + entity_type)
            new_tokens.append(token)
            last_entity = entity_type

    return pd.DataFrame({"Token": new_tokens, "Label": new_labels})
# 转换
train_bio = convert_to_BIO(train_df)
dev_bio = convert_to_BIO(dev_df)

# 保存
train_bio.to_csv("final_train_BIO.csv", index=False)
dev_bio.to_csv("final_dev_BIO.csv", index=False)

print("✅ 转换完成，已经保存为 final_train_BIO.csv 和 final_dev_BIO.csv")