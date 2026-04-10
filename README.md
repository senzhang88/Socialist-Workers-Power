# WorkPowers / 劳动者力量

> 一个专为上海地区劳动者设计的维权知识库与工具集。
> 
> **品牌统一：** WorkPowers = 劳动者力量
> 
> **核心理念：** 企业有法务团队，而员工只有自己——这个项目的目标就是补上这个信息差。

[![GitHub stars](https://img.shields.io/github/stars/senzhang88/Socialist-Workers-Power?style=social)](https://github.com/senzhang88/Socialist-Workers-Power/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/senzhang88/Socialist-Workers-Power?style=social)](https://github.com/senzhang88/Socialist-Workers-Power/network)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()
[![Location: Shanghai](https://img.shields.io/badge/Location-Shanghai-blue.svg)]()
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-purple.svg)](https://github.com/senzhang88/Socialist-Workers-Power/releases)

---

## ⚡ 最快使用方式：Claude Skill（一键安装）

**一句话安装：**
```bash
claude skills install https://github.com/senzhang88/Socialist-Workers-Power/releases/latest/download/work-powers-shanghai-v1.0.skill
```

**然后直接问 Claude：**
- "公司让我停岗待业怎么办"
- "帮我算一下赔偿金额"  
- "怎么申请劳动仲裁"
- "被口头辞退了怎么取证"

**✅ 无需配置，无需学习，对话即服务**

---

## 🚀 快速开始

### 方式1：作为Claude Skill使用（强烈推荐 - 最简单）

**一键安装：**
```bash
claude skills install https://github.com/senzhang88/Socialist-Workers-Power/releases/latest/download/work-powers-shanghai-v1.0.skill
```

**或手动安装：**
```bash
# 1. 下载 .skill 文件
wget https://github.com/senzhang88/Socialist-Workers-Power/releases/latest/download/work-powers-shanghai-v1.0.skill

# 2. 安装到 Claude
claude skills install work-powers-shanghai-v1.0.skill

# 或解压到技能目录
unzip work-powers-shanghai-v1.0.skill -d ~/.claude/skills/work-powers-shanghai/
```

**使用方法：**
安装后，在 Claude 对话中提及劳动维权相关问题即可自动触发：
- "公司让我停岗待业怎么办"
- "帮我算一下赔偿金额"
- "怎么申请劳动仲裁"

### 方式2：直接使用文档

- 按维权阶段查阅 `docs/` 目录下的指南
- 使用 `tools/compensation-calculator.py` 计算赔偿金额
- 查阅 `resources/official-resources.md` 获取官方渠道

---

## 📁 项目结构

```
Socialist-Workers-Power/
├── README.md                           # 项目总览（本文件）
├── LICENSE                             # MIT开源协议
├── CHANGELOG.md                        # 版本更新记录
│
├── skill/                              # 🎯 Claude技能包（Anthropic官方标准）
│   ├── SKILL.md                        # 技能主文件
│   ├── CLAUDE.md                       # Claude代理使用说明
│   ├── docs/                           # 阶段指南
│   ├── references/                     # 参考资料
│   ├── scripts/                        # 可执行脚本
│   ├── agents/                         # 评估代理
│   ├── evals/                          # 测试用例
│   └── eval-viewer/                    # 可视化查看器
│
├── releases/                           # 📦 技能发布包
│   └── work-powers-shanghai-v1.0.skill # 一键安装包
│
├── docs/                               # 📚 按维权阶段组织的完整文档
│   ├── phase-0-prepare/                # 🛡️ 预防阶段
│   │   ├── handbook-self-check.md       # 员工手册自查清单
│   │   └── job-offer-checklist.md     # ⭐ 入职避雷指南
│   │
│   ├── phase-1-crisis/                 # ⚠️ 危机识别阶段
│   │   ├── soft-layoff-guide.md        # 软裁员/变相辞退应对
│   │   └── tech-company-risks.md       # 互联网公司风险
│   │
│   ├── phase-2-evidence/               # 📸 证据收集阶段
│   │   ├── evidence-checklist.md       # 证据分级清单
│   │   └── recording-guide.md         # ⭐ 录音取证指南
│   │
│   ├── phase-3-action/                 # ⚔️ 行动阶段
│   │   ├── arbitration-guide.md        # 劳动仲裁全流程
│   │   └── templates.md                # 文书模板
│   │
│   ├── phase-4-court/                  # ⚖️ 开庭阶段
│   │   └── hearing-guide.md           # 开庭指南
│   │
│   └── phase-5-post/                   # ✅ 后续阶段
│       └── (待补充)
│
├── references/                         # 参考资料（按类型组织）
│   ├── laws/                          # 📚 法律法规
│   │   └── laws-compilation.md        # 核心法律条文汇编
│   │
│   ├── shanghai/                      # 🏙️ 上海地方规定
│   │   ├── shanghai-regulations.md    # 上海劳动法特殊规定
│   │   └── shanghai-social-insurance.md # 社保公积金政策
│   │
│   └── compensation/                  # 💰 赔偿计算
│       └── compensation-calc.md       # 计算指南与案例
│
├── tools/                             # 🛠️ 实用工具
│   └── compensation-calculator.py     # ⭐ 赔偿计算器
│
└── resources/                          # 🌐 外部资源
    └── official-resources.md          # 官方渠道导航
```

---

## 🎯 核心功能

### 1. 按维权阶段导航

无论你在哪个阶段，都能找到对应指南：

| 阶段 | 适用场景 | 关键文档 |
|------|---------|---------|
| **Phase 0: 预防** | 入职前、合同审查 | `job-offer-checklist.md` |
| **Phase 1: 危机** | 发现被针对、软裁员 | `soft-layoff-guide.md` |
| **Phase 2: 证据** | 收集证据、录音取证 | `recording-guide.md` |
| **Phase 3: 行动** | 申请仲裁、写申请书 | `arbitration-guide.md` |
| **Phase 4: 开庭** | 准备开庭、质证答辩 | `hearing-guide.md` |

### 2. 上海专属数据（2025-2026）

| 数据项 | 数值 | 适用期间 |
|--------|------|---------|
| **2024年度社平工资** | 12,434元/月 | 2025.07-2026.06 |
| **三倍封顶** | 37,302元/月 | 2025.07-2026.06 |
| **社保基数下限** | 7,460元/月 | 2025.07-2026.06 |
| **最低工资** | 2,690元/月 | 2023.07起 |
| **产假天数** | 158天起 | 长期 |

### 3. 实战工具

**赔偿计算器**（`tools/compensation-calculator.py`）：
```bash
$ python tools/compensation-calculator.py

=== 上海劳动仲裁赔偿计算器 ===
请输入入职日期（格式：YYYY-MM-DD）：2020-03-15
请输入离职日期（格式：YYYY-MM-DD）：2025-03-15
请输入月薪（元）：8000
是否违法解除？（y/n）：y

计算结果：
- 工作年限：5年1个月 = 5.5年
- 经济补偿金（N）：44,000元
- 违法解除赔偿金（2N）：88,000元 ⭐
```

---

## 📊 内容统计

- **文档总数**：14个专业指南
- **总字数**：约30,000+字
- **覆盖法条**：50+条核心法律条文
- **案例模板**：10+份实战文书
- **数据更新**：2025年4月

---

## ⚡ 特色亮点

### 🎯 可执行优先

不说"根据劳动合同法第XX条"，而是告诉你：
- ✅ "今天该做什么"
- ✅ "明天该做什么"  
- ✅ "本周内要完成什么"

### 🛡️ 全流程覆盖

从**入职避雷** → **危机识别** → **证据固定** → **仲裁申请** → **开庭应对** → **强制执行**，每一步都有指南。

### 📦 开箱即用

- 所有法规原文内置，无需联网查询
- 文书模板可直接复制使用
- 计算器本地运行，数据安全

### 🔒 隐私保护

- 纯本地工具，数据不上传
- 开源代码，可审计
- 无追踪、无广告

---

## 📖 推荐阅读路径

### 如果你正遭遇软裁员
1. `docs/phase-1-crisis/soft-layoff-guide.md` - 了解应对策略
2. `docs/phase-2-evidence/recording-guide.md` - 学习取证技巧
3. `tools/compensation-calculator.py` - 计算赔偿金额
4. `docs/phase-3-action/arbitration-guide.md` - 申请仲裁

### 如果你准备入职新公司
1. `docs/phase-0-prepare/job-offer-checklist.md` - 入职前调查
2. `docs/phase-0-prepare/handbook-self-check.md` - 手册自查
3. `resources/official-resources.md` - 查企业背景

### 如果你是HR/法务
- 本项目也可以帮你了解劳动者视角，优化合规流程

---

## 🌐 参与贡献

我们欢迎通过以下方式参与项目：

### 如何贡献
- **发现错误？** → 提交 [GitHub Issue](https://github.com/senzhang88/Socialist-Workers-Power/issues)
- **有改进建议？** → 提交 Pull Request
- **想分享案例？** → 发送邮件至 zhsheshhh@gmail.com（我们会脱敏处理后纳入）

### 贡献原则
1. **GitHub为主**：所有正式文档以GitHub版本为准
2. **脱敏处理**：案例分享前删除敏感信息（公司名称、个人姓名等）
3. **版权归属**：所有贡献内容默认采用MIT协议开源

---

## ⚠️ 重要声明

1. **法律咨询免责声明**：本项目提供的仅为法律信息整理和维权流程指导，**不构成法律意见或律师服务**。

2. **具体情况差异**：劳动争议具体情况复杂，建议必要时咨询专业劳动法律师。

3. **政策时效性**：各地执法口径可能存在差异，法律法规会更新，请以当地实际规定为准。

4. **证据责任**：证据收集需合法合规，非法取证可能导致证据无效甚至法律责任。

---

## 🤝 贡献指南

欢迎提交 Issue 和 PR：
- 补充地方规定（其他省市）
- 更新法律法规
- 添加典型案例
- 优化工具功能

### 贡献步骤
1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📜 开源协议

本项目采用 [MIT License](LICENSE) - 自由使用、修改、分发。

---

## 🙏 致谢

- 感谢所有劳动者的真实反馈
- 感谢开源社区的法律知识分享
- 感谢上海地区律师和仲裁员的实践指导

---

## 📞 联系与支持

- **GitHub Issues**：提交问题或建议
- **Email**：zhsheshhh@gmail.com
- **微信社群**：（待建立）

---

<div align="center">

**记住：企业有法务团队，而员工只有自己。**

**这个项目希望能帮到你。**

⭐ 如果这个项目对你有帮助，请给个 Star！

</div>
