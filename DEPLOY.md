# 部署说明（shawarmai.com）

## 1. GitHub 仓库配置

在 GitHub 仓库 **Settings → Secrets and variables → Actions** 中新增 Secret：

| 名称 | 说明 |
|------|------|
| `SSH_PRIVATE_KEY` | 用于登录 `root@shawarmai.com` 的 SSH 私钥完整内容（包含 `-----BEGIN ... -----` 和 `-----END ... -----`） |

## 2. 触发部署

- **自动**：推送到 `main` 分支时会自动部署。
- **手动**：在 **Actions** 页选择 “Deploy to shawarmai.com”，点击 “Run workflow”。

## 3. 服务器端（首次部署前建议准备）

- 部署目录默认为：`/var/www/stable_emo`（可在 `.github/workflows/deploy.yml` 的 `env.REMOTE_PATH` 修改）。
- 确保服务器已安装：`python3`、`pip`/`pip3`。
- 应用需环境变量 `OPENAI_API_KEY`，可在服务器上配置：
  - 方式一：在 `/var/www/stable_emo` 下建 `.env` 并在启动前 `export` 或使用 `python-dotenv`。
  - 方式二：用 systemd 时在 service 里写 `Environment=OPENAI_API_KEY=sk-...`。

## 4. 使用 systemd（推荐）

若已创建 systemd 服务（如 `stable_emo.service`），可在 workflow 里把 “Install deps and restart” 步骤改为：

```yaml
run: |
  ssh -i ~/.ssh/deploy_key -o StrictHostKeyChecking=no \
    ${{ env.REMOTE_USER }}@${{ env.REMOTE_HOST }} \
    "cd ${{ env.REMOTE_PATH }} && pip3 install -r requirements.txt -q && sudo systemctl restart stable_emo"
```

并删除其中的 `pkill` 和 `nohup gunicorn ...` 行。
