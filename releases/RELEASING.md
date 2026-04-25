# 发布流程 — 持续可复用版

> 适用于 WorkPowers / 劳动者力量 Skill 的版本发布。
> 当前最新：[v1.1](./notes/v1.1.md)（2026-04-26）。

---

## 角色分工

- **GitHub 账户**：`senzhang88`（仓库归属）
- **本机 SSH key**：`~/.ssh/id_ed25519_senzhang88`（已绑定 senzhang88 账户）
- **gh CLI**：`senzhang88` + `zhangsensen` 双账号在线，默认 senzhang88（`gh auth status` 检查）

---

## 发布前清单

- [ ] 所有要发布的内容已 commit 到 main
- [ ] `mkdocs build --strict` 通过（如改动涉及 `docs/`）
- [ ] `python skill/scripts/calculator.py --start 2020-01-01 --end 2025-01-01 --salary 10000 --illegal` 烟测通过
- [ ] CHANGELOG.md 顶部加新版本段落（Keep a Changelog 格式）
- [ ] 同步以下文件的版本号：
  - `skill/SKILL.md` footer
  - `skill/CLAUDE.md` footer
  - `skill/README.md` 顶部 v1.X 段
  - `skill/ITERATION_LOG.md` 末尾版本表

---

## 发布步骤（每次照抄）

### 1. 打包 .skill 制品

```bash
cd skill && zip -rq ../releases/work-powers-shanghai-vX.Y.skill . \
  -x ".*" "*.pyc" "__pycache__/*" "logs/*" && cd ..

# 验证
unzip -l releases/work-powers-shanghai-vX.Y.skill | tail -3
sha256sum releases/work-powers-shanghai-vX.Y.skill
```

### 2. Commit + 打 tag

```bash
git add CHANGELOG.md releases/work-powers-shanghai-vX.Y.skill releases/notes/vX.Y.md
git commit -m "release(skill): vX.Y.0 — <一句话总结>"

git tag -a vX.Y -m "vX.Y.0 — <一句话总结>"
```

### 3. Push

```bash
# 如果 SSH 连接缓存有问题，先清掉再推
rm -f ~/.ssh/cm-git@github.com:22

git push origin main
git push origin vX.Y
```

### 4. 创建 GitHub Release

```bash
# 先确认 gh 当前账户是 senzhang88
gh auth status | head -3
# 如果不是 senzhang88：
# gh auth switch -h github.com -u senzhang88

gh release create vX.Y \
  --repo senzhang88/Socialist-Workers-Power \
  --title "vX.Y.0 — <一句话总结>" \
  -F releases/notes/vX.Y.md \
  releases/work-powers-shanghai-vX.Y.skill
```

### 5. 验证

```bash
gh release view vX.Y --repo senzhang88/Socialist-Workers-Power
```

发布后链接：

```
https://github.com/senzhang88/Socialist-Workers-Power/releases/tag/vX.Y
https://github.com/senzhang88/Socialist-Workers-Power/releases/download/vX.Y/work-powers-shanghai-vX.Y.skill
```

---

## Release Notes 模板

写新版本时复制 [notes/v1.1.md](./notes/v1.1.md) 当模板，至少包含：

1. **核心升级摘要**（一段话）
2. **一键安装命令**
3. **新增功能**（按文件 + 行数说明，给读者看到内容厚度）
4. **解决了什么问题**（vX-1 哪些缺口被补上）
5. **Breaking Changes**（如有）
6. **下一步路线图**（vX+1 计划）
7. **下载 + SHA256**

---

## 已知问题排查

### 推送被 GitHub 拒绝（zhangsensen denied）

清掉 SSH 连接缓存重试：

```bash
rm -f ~/.ssh/cm-git@github.com:22
ssh -T github-senzhang88   # 应返回 Hi senzhang88!
```

### gh CLI 无权创建 release

```bash
gh auth status
# 确认 senzhang88 是 active；不是的话切：
gh auth switch -h github.com -u senzhang88
```

### deploy.sh 显示在 git status

deploy.sh 含服务器 IP，**永不进 git**。它现在是 untracked 状态由 .gitignore 边界外但**不被 commit**——继续用即可，commit 时**永远不要 `git add deploy.sh`**。

如果 `git add .` 误把它加进去，跑 `git restore --staged deploy.sh` 撤销。

---

## 屏蔽边界（绝不进仓库的内容）

详见根目录 [`.gitignore`](../.gitignore) —— 涵盖：

- 7 个个人案件目录（仲裁加投诉 / 期权争议 等）
- SERVER_ACCESS.md / SSH 凭据 / API 密钥
- wenshu_downloads/（裁判文书原始 HTML）
- 编辑器/AI 工具本地配置
- opc入住/ 下的 docx 与本地状态

发布前再扫一次：

```bash
git diff --stat origin/main..HEAD | grep -iE "案例|期权|名誉|个人|档案" || echo "✅ 安全"
```

---

## 历史发布

- [v1.1](./notes/v1.1.md) — 2026-04-26 — 接入判例知识库 + 6 大高频场景模板
- v1.0 — 2025-03-15 — 初始公开发布（无独立 notes 文件）
