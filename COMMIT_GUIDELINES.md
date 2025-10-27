# Git Commit 规范

## 提交信息格式

### 类型（Type）
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整（不影响代码运行）
- `refactor`: 重构代码
- `test`: 添加测试
- `chore`: 构建过程或辅助工具的变动

### 示例

```
feat: Add trip editor basic info component
fix: Resolve trip tree layout overlap issue
docs: Add ACApp deployment guide
style: Format title input with larger font and center alignment
refactor: Replace Axios with native Fetch API
chore: Update dependencies
```

### 提交信息规则

1. **语言**: 所有提交信息使用英文
2. **格式**: `<type>: <description>`
3. **长度**: 描述不超过50字符
4. **时态**: 使用祈使语气（如 "Add", "Fix", "Update"）

### 常见错误

❌ 错误示例：
```
chore: 更新依赖
fix: 修复旅行树布局重叠问题
feat: 添加旅行编辑器
```

✅ 正确示例：
```
chore: Update dependencies
fix: Resolve trip tree layout overlap
feat: Add trip editor component
```

