---

### ② `src/lambda_function.py`
Lambdaで実行されるメインのPythonスクリプトです。

```python
import os
import json
import urllib.request
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    webhook_url = os.environ.get('WEBHOOK_URL')
    
    if not webhook_url:
        logger.error("WEBHOOK_URL environment variable is not set.")
        return {'statusCode': 500, 'body': 'Configuration error'}

    # 定期チェック対象のサンプルURL
    target_site = "https://httpbin.org/status/200"
    
    try:
        req = urllib.request.Request(target_site)
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            message = f"【自動点検】対象サイトの正常稼働を確認しました。(Status: {status_code})"
    except Exception as e:
        logger.error(f"Failed to check site: {str(e)}")
        message = f"【警告】対象サイトへの接続に失敗しました: {str(e)}"

    # Webhook送信処理
    payload = {"text": message}
    data = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    
    try:
        notice_req = urllib.request.Request(webhook_url, data=data, headers=headers)
        with urllib.request.urlopen(notice_req) as notice_res:
            logger.info("Notification sent successfully.")
            return {'statusCode': 200, 'body': 'Success'}
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
        return {'statusCode': 500, 'body': 'Notification failed'}