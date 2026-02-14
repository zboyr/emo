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

## 在 Runner 上部署（GitHub Actions）

1. 把本仓库推送到 GitHub（可先 `git init` 并添加远程）。
2. 在仓库 **Settings → Secrets and variables → Actions** 里新增 Secret：
   - Name: `OPENAI_API_KEY`
   - Value: 你的 OpenAI API Key（不要提交到代码里）。
3. 推送 `main` 或 `master` 分支，或在该仓库 **Actions** 里手动运行 **Deploy on Runner**。
4. 工作流会在 Runner 上安装依赖并执行 `python app.py`，应用在本次任务期间会一直运行（任务默认最长约 6 小时）。

注意：GitHub 提供的 Runner 通常无法从外网直接访问；若需要公网可访问，请使用自托管 Runner 或部署到云主机/容器。
