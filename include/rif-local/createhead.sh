#!/bin/bash

# 检查是否提供了文件路径
if [ $# -lt 1 ]; then
  echo "用法: $0 文件路径"
  exit 1
fi

# 输入文件路径
input_file=$1

# 遍历文件的每一行
while IFS= read -r line || [[ -n "$line" ]]; do
  # 去掉行首和行尾的空格（可选）
  trimmed_line=$(echo "$line" | xargs)
  
  # 如果行为空，跳过
  if [ -z "$trimmed_line" ]; then
    continue
  fi

  # 创建文件
  touch "$trimmed_line"
  echo "已创建文件: $trimmed_line"
done < "$input_file"

echo "所有文件已创建完毕！"
