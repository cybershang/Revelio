import json

# 初始化数据列表
data = []

# 生成 3000 行数据
for i in range(1, 3001):
    video_id = f"{i}.mp4"  # 第一列 'video_id'
    if 1 <= i <= 1000:
        is_violence = 0  # 第二列 'is_violence'
    elif 1001 <= i <= 2500:
        is_violence = 1
    else:
        is_violence = 0

    # 第三列 'detection result' 先初始化为 None
    detection_result = None
    # 第四到七列先初始化为 None
    true_positive = None
    true_negative = None
    false_negative = None
    false_positive = None

    # 创建一行数据的字典
    row = {
        "video_id": video_id,
        "is_violence": is_violence,
        "detection result": detection_result,
        "true positive": true_positive,
        "true negative": true_negative,
        "false negative": false_negative,
        "false positive": false_positive
    }
    data.append(row)

# 将数据保存为 JSON 文件
with open('ground_truth.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Successfully generating ground truth！")
