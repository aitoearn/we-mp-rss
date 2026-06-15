# WeRSS 知识库元数据

> 本文件是知识库的「灵魂层」配置入口，供 LLM 与 Skills 自动发现路径与约定。

## 基本信息

| 字段 | 值 |
|------|-----|
| 名称 | we-mp-rss-kb |
| 描述 | WeRSS 微信公众号 RSS 订阅助手专属 LLM-Wiki 知识库 |
| 版本 | v0.1.0 |
| 创建日期 | 2026-06-13 |
| 维护者 | LLM（写入）/ 人（只读） |

## 路径配置

| 路径类型 | 相对路径 | 说明 |
|----------|----------|------|
| 知识库根目录 | `.` | 当前 vault 根目录 |
| 代码仓库 | `..` | we-mp-rss 项目根目录 |
| 原始文档源 | `../docs` | 项目 docs/ 目录（只读） |
| 扩展文档源 | `../.qoder/repowiki/zh/content` | Qoder 生成的 Wiki 草稿（只读，待校验） |
| 输出目录 | `docs/plans` | 技术方案等产物输出路径 |
| 查询存档 | `queries/` | 有价值问答的沉淀目录 |

## 关联知识库

```yaml
relatedKBs: []
```

## 页面类型约定

| type | 目录 | 用途 |
|------|------|------|
| entity | entities/ | 数据实体（表、文件型存储） |
| concept | concepts/ | 业务/技术概念 |
| source | sources/ | 原始文档摘要 |
| module | code/modules/ | 代码模块概述 |
| class | code/classes/ | 核心类详情 |
| query | queries/ | 问答沉淀 |
| diagram | code/diagrams/ | 架构图与调用链 |

## Frontmatter 规范

```yaml
---
type: entity | concept | source | module | class | query | diagram
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
related: []
source_file: 相对路径（source 类型必填）
---
```

## 检索建议

1. 先读 `index.md` 定位主题
2. 业务问题 → `concepts/`
3. 数据结构 → `entities/`
4. 代码实现 → `code/modules/`、`code/classes/`
5. 历史设计 → `sources/`
6. 已有问答 → `queries/`
