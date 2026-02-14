# 亲密关系 · 情绪稳定判断

用 OpenAI 判断：在用户描述的亲密关系情形下，是否应该保持情绪稳定。仅输出 **Y**（是）或 **N**（否）。

- 兼容手机和电脑的响应式页面
- 英文提示词 + 低 temperature，保证输出一致

## 本地运行

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY="你的密钥"
python app.py
```

浏览器打开 http://localhost:5000

## 在自托管 Runner 上部署（GitHub Actions + systemd）

1. 在服务器上注册 **self-hosted runner**（label: `self-hosted`），把本仓库推送到 GitHub。
2. 在仓库 **Settings → Secrets and variables → Actions** 里新增 Secret：`OPENAI_API_KEY`。
3. 推送 `main` / `master` 或在 **Actions** 里手动运行 **Deploy on Self-Hosted Runner**。
4. 工作流会把应用部署到 **`$HOME/emo`**，并用 **systemd 用户服务** 常驻运行（端口 13942）。

**保证服务在无登录时也运行**（在部署用的那台机上执行一次）：

```bash
loginctl enable-linger $(whoami)
```

查看/重启服务：

```bash
systemctl --user status emo
systemctl --user restart emo
```
