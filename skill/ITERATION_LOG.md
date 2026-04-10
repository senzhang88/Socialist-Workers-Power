# 技能迭代日志

## 迭代目标

根据Anthropic官方skill-creator最佳实践，将labor-rights-shanghai技能优化至生产就绪状态。

## 迭代1：基础架构完善

**日期**: 2025-04-10

### 变更内容

1. **重构SKILL.md**
   - 添加标准YAML frontmatter（name, description, compatibility）
   - 优化description，在前200字符包含核心触发场景
   - 添加`compatibility: universal`声明

2. **创建agents/目录**
   - `grader.md`: 五维度评分代理（可执行性/准确性/完整性/立场/工具使用）
   - `comparator.md`: 版本比较代理，评估改进效果
   - `analyzer.md`: 数据分析代理，识别系统性问题

3. **创建evals/目录**
   - `evals.json`: 8个测试用例，覆盖主要维权场景
     - 软裁员应对
     - 赔偿计算（普通/高收入封顶）
     - 仲裁申请流程
     - 证据收集
     - 加班费争议
     - 试用期辞退
     - 上海数据准确性

4. **创建scripts/aggregate_benchmark.py**
   - 聚合多轮评估结果
   - 统计各维度平均分/通过失败率/常见问题

5. **创建eval-viewer/generate_review.py**
   - 生成HTML可视化报告
   - 包含维度评分条/常见问题/详细结果

### 评估结果

```bash
python scripts/aggregate_benchmark.py logs/iteration-1/*.json
```

**汇总**:
- 总测试数: 3（示例数据）
- 通过: 2 (66.7%)
- 失败: 1 (33.3%)

**维度评分**:
| 维度 | 平均分 | 问题 |
|------|--------|------|
| 可执行性 | 4.7 | 良好 |
| 准确性 | 4.3 | 工作年限计算说明需改进 |
| 完整性 | 3.7 | 遗漏仲裁时效提醒 |
| 立场 | 5.0 | 优秀 |
| 工具使用 | 3.0 | 需增强计算器调用 |

**主要问题**:
1. ⚠️ 仲裁时效提醒遗漏（严重性：高）
2. ⚠️ 工具调用率偏低（40%）
3. ⚠️ 工作年限计算说明不够清晰

### 下一步计划

**迭代2重点**:
- [ ] 在SKILL.md前50行添加粗体时效提醒
- [ ] 优化模板，明确提示使用calculator.py
- [ ] 在description中添加"仲裁时效"关键词以提高触发

---

## 迭代流程指南

### 如何运行评估

```bash
# 1. 运行单轮评估（手动或通过Claude调用）
# 将评估结果保存到 logs/iteration-N/XXX.json

# 2. 聚合评估结果
cd ~/.claude/skills/labor-rights-shanghai
python scripts/aggregate_benchmark.py 'logs/iteration-1/*.json'

# 3. 生成可视化报告
python eval-viewer/generate_review.py aggregated-results.json -o report.html
open report.html
```

### 如何对比迭代

使用`agents/comparator.md`指导，对比两个版本的SKILL.md响应差异，评估改进效果。

### 如何优化description

使用`agents/analyzer.md`分析触发率问题，优化description前200字符的关键词密度。

---

## 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| v1.0 | 2025-04-10 | 初始版本，按官方标准重构 |
