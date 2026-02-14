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
2. **Runner 所用系统用户需具备无密码 sudo**（用于安装/重启 systemd 服务），例如：
   ```bash
   # 在服务器上执行（将 runner 换成实际运行 Actions 的用户名）
   echo 'runner ALL=(ALL) NOPASSWD: /usr/bin/systemctl, /usr/bin/tee' >> /etc/sudoers.d/emo
   ```
3. 在仓库 **Settings → Secrets and variables → Actions** 里新增 Secret：`OPENAI_API_KEY`。
4. 推送 `main` / `master` 或在 **Actions** 里手动运行 **Deploy on Self-Hosted Runner**。
5. 工作流会把应用部署到 **`$HOME/emo`**，并用 **systemd 系统服务** 常驻运行（端口 13942），不依赖 D-Bus/用户会话。

查看/重启服务：

```bash
sudo systemctl status emo
sudo systemctl restart emo
```
