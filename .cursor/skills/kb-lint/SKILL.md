---
name: kb-lint
description: 巡检 we-mp-rss-kb 知识库健康度：矛盾、孤页、死链、缺失概念、过时内容。Use when checking KB quality or after bulk updates.
---

# kb-lint 知识库巡检

## Overview

定期自检 Wiki 结构健康度。遵循 `we-mp-rss-kb/CLAUDE.md` 的 Lint 流程。

## 检查项

| # | 检查 | 方法 |
|---|------|------|
| 1 | 矛盾 | 对比不同页面描述，代码仓优先 |
| 2 | 孤页 | 无 inbound `[[链接]]` 的页面 |
| 3 | 死链 | 引用 `[[页面]]` 但目标不存在 |
| 4 | 缺失 | 被提及但未独立成页的概念/实体 |
| 5 | 过时 | 代码已变更但 Wiki 未更新 |
| 6 | Frontmatter | type/created/updated 是否齐全 |
| 7 | 短页 | 内容少于 5 行的页面 |

## 流程

1. 读取 `index.md` 获取全量页面列表
2. 逐目录扫描：`concepts/`、`entities/`、`sources/`、`code/`
3. 交叉检查链接完整性
4. 抽样对比代码仓关键文件（models、apis 路由）
5. 输出问题清单 + 修复建议

## 输出格式

```markdown
## 巡检报告 YYYY-MM-DD

### 通过项
- ...

### 问题清单
| 优先级 | 类型 | 页面 | 问题 | 建议修复 |
|--------|------|------|------|----------|

### 统计
- 总页数 / 孤页数 / 死链数 / 缺失概念数
```

## 修复后

- 执行修复 → 更新 `log.md`
- 建议用户运行 kb-query 验证关键页面
