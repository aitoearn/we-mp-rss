# WeRSS LLM-Wiki 知识库

基于 [LLM-Wiki 架构](https://github.com/karpathy/llm-wiki) 构建的 WeRSS 专属知识库。

## 三层架构

| 层 | 内容 | 位置 |
|----|------|------|
| L1 Sources | 原始文档/代码（只读） | `../docs/`、`..`（代码仓） |
| L2 Wiki | LLM 维护的 markdown | 本目录 |
| L3 Schema | 工作规范 | `CLAUDE.md`、`KB-META.md` |

## Obsidian 使用

1. 下载 [Obsidian](https://obsidian.md/)
2. 「打开文件夹」→ 选择本目录 `we-mp-rss-kb/`
3. 开启图谱视图查看知识网络

## Cursor Skills

项目 `.cursor/skills/` 下已配置：

| Skill | 用途 |
|-------|------|
| `kb-just-ask` | 全能管家，直接提问 |
| `kb-ingest` | 摄入新文档/代码变更 |
| `kb-query` | 基于 Wiki 回答问题 |
| `kb-lint` | 巡检知识库健康度 |
| `kb-sync` | 同步远程/增量更新 |

## 快速开始

```
# 直接提问
使用 kb-just-ask：WeRSS 的采集流程是什么？

# 摄入新文档
使用 kb-ingest：摄入 ../docs/dingyue.md

# 巡检
使用 kb-lint：巡检知识库
```

## 目录结构

```
we-mp-rss-kb/
├── KB-META.md       # 元数据与路径配置
├── CLAUDE.md        # LLM 工作规范（Schema）
├── index.md         # 内容索引
├── log.md           # 操作日志
├── concepts/        # 业务/技术概念
├── entities/        # 数据实体
├── sources/         # 文档摘要
├── code/
│   ├── modules/     # 代码模块
│   └── diagrams/    # 架构图
└── queries/         # 问答沉淀
```
