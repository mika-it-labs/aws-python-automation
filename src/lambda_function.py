import os
import json
import urllib.request
import urllib.parse
import logging

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambdaエントリーポイント
    環境変数からSlack / LINE等のWebhook URLを取得し、通知を送信する
    """
    webhook_url = os.environ.get('WEBHOOK_URL')
    
    if not webhook_url:
        logger.error("WEBHOOK_URL environment variable is not set.")
        return {'statusCode': 500, 'body': 'Configuration error'}

    # 1. 自動収集・チェックしたいデータ（例: 監視対象のステータスチェックや情報取得）
    # ここでは例としてシンプルなチェック処理を実施
    target_site = "https://httpbin.org/status/200"
    
    try:
        req = urllib.request.Request(target_site)
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            message = f"【自動点検レポート】対象サイトの正常稼働を確認しました。(Status: {status_code})"
    except Exception as e:
        logger.error(f"Failed to check site: {str(e)}")
        message = f"【警告】対象サイトのアクセスに失敗しました: {str(e)}"

    # 2. Incoming Webhook経由で通知を送信 (Slack / Incoming Webhook対応)
    payload = {
        "text": message
    }
    
    data = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    
    try:
        notice_req = urllib.request.Request(webhook_url, data=data, headers=headers)
        with urllib.request.urlopen(notice_req) as notice_res:
            logger.info("Notification sent successfully.")
            return {
                'statusCode': 200,
                'body': json.dumps('Successfully executed and notified!')
            }
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to send notification')
        }
