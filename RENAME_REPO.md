# 如何重命名GitHub仓库

## 当前状态
- **本地文件夹名称**: `roamio` ✅
- **GitHub仓库名称**: `cet` ❌
- **远程URL**: `git@github.com:ppshuX/cet.git`

## 解决方案

### 方案1：在GitHub上重命名（推荐）

#### 步骤1：重命名GitHub仓库
1. 访问 https://github.com/ppshuX/cet/settings
2. 滚动到"Repository name"部分
3. 将名称从 `cet` 改为 `roamio`
4. 点击"Rename"按钮

#### 步骤2：更新本地远程URL
```bash
# 更新远程URL
git remote set-url origin git@github.com:ppshuX/roamio.git

# 验证
git remote -v
```

#### 步骤3：推送所有更改
```bash
git push -u origin master
```

### 方案2：创建新仓库（如果方案1失败）

#### 步骤1：在GitHub上创建新仓库
1. 访问 https://github.com/new
2. 仓库名称: `roamio`
3. 描述: "Travel planning and sharing platform"
4. 设为Public或Private
5. **不要**勾选"Initialize with a README"
6. 点击"Create repository"

#### 步骤2：更新远程URL并推送
```bash
# 删除旧的远程
git remote remove origin

# 添加新的远程
git remote add origin git@github.com:ppshuX/roamio.git

# 推送所有分支
git push -u origin master

# 如果master分支已废弃，推送所有分支
git push -u origin --all
```

### 验证
```bash
# 检查远程配置
git remote -v

# 应该显示：
# origin  git@github.com:ppshuX/roamio.git (fetch)
# origin  git@github.com:ppshuX/roamio.git (push)
```

### 注意事项
- 重命名后，旧的URL仍然会重定向到新URL（GitHub自动处理）
- 如果有其他协作者，需要通知他们更新URL
- Webhooks、CI/CD配置可能需要更新

