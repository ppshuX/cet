#!/bin/bash

# 设置备份目录
BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="backup_${DATE}.tar.gz"

# 要备份的文件或文件夹
DB_FILE="db.sqlite3"
MEDIA_DIR="media"

# 创建备份目录（如果不存在）
mkdir -p $BACKUP_DIR

# 检查数据库文件是否存在
if [ ! -f "$DB_FILE" ]; then
    echo "❌ 没找到数据库文件：$DB_FILE"
    exit 1
fi

# 创建压缩包（包含数据库和 media 目录）
tar -czf "$BACKUP_DIR/$FILENAME" "$DB_FILE" "$MEDIA_DIR" 2>/dev/null

# 结果输出
if [ $? -eq 0 ]; then
    echo "✅ 备份成功：$BACKUP_DIR/$FILENAME"
else
    echo "⚠️ 备份时出错，请检查 media 目录是否存在。"
fi

