import os

# 创建目录结构
dirs = ['ui', 'core', 'utils']
for d in dirs:
    if not os.path.exists(d):
        os.makedirs(d)
        print(f"创建目录: {d}")
    else:
        print(f"目录已存在: {d}")

print("目录结构创建完成！")
