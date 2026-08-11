# AWS + Python + Terraform 自動化通知システム

## 概要
AWS Lambda、Python、Terraform（IaC）を使用して、指定したWebサイトのステータスチェックや情報取得を行い、結果をSlack/LINE（Webhook）へ自動通知するサーバーレスシステムです。

## システム構成
- **Infrastructure as Code:** Terraform
- **Compute:** AWS Lambda (Python 3.12)
- **Scheduler:** Amazon EventBridge (毎日定時実行)
- **Notification:** Incoming Webhook (Slack / LINE)

```mermaid
flowchart LR
    EB["Amazon EventBridge (スケジュール実行)"] -->|トリガー| Lambda["AWS Lambda (Python 3.12)"]
    Lambda -->|データチェック| Site["対象Webサイト (ステータス確認)"]
    Lambda -->|POSTリクエスト| Webhook["Incoming Webhook (Slack / LINE)"]

    style EB fill:#FF9900,stroke:#333,stroke-width:1px,color:#fff
    style Lambda fill:#FF9900,stroke:#333,stroke-width:1px,color:#fff
    style Webhook fill:#4A154B,stroke:#333,stroke-width:1px,color:#fff
*(※ 改行文字 `\n` や日本語が含まれるラベル部分を `""`（ダブルクォーテーション）で囲む形式に修正し、より構文エラーが起きにくい形式に整えました。)*

---

### 保存してGitHubへ送信するコマンド

`README.md` を保存（`Ctrl` + `S`）したら、PowerShellで以下のコマンドだけを実行します。

```
powershell
git add README.md
git commit -m "fix: Correct Mermaid diagram syntax in README"
git push

## 特徴・工夫した点
1. **完全コード化（IaC）:** インフラリソースの作成からIAM権限の付与まで、すべてTerraformで管理・自動化。
2. **無償枠での運用:** サーバーレス構成を採用し、ランニングコスト0円で運用可能。
3. **機密情報の保護:** Webhook URLなどの機密情報はコードへ直書きせず、環境変数経由で注入。

## フォルダ構成
```text
.
├── README.md
├── src/
│   └── lambda_function.py
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── .gitignore