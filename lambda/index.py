# lambda/index.py
import json
import os
import re
from urllib import request

# 環境変数で FastAPI エンドポイントを指定
FASTAPI_URL = os.environ.get("FASTAPI_URL", "https://7527-35-221-196-178.ngrok-free.app/infer")

# Lambda ハンドラ
def lambda_handler(event, context):
    try:
        # リクエストボディの解析
        body = json.loads(event.get('body', '{}'))
        message = body.get('message', '')
        conversation_history = body.get('conversationHistory', [])

        # FastAPI に渡すペイロードを構築
        payload = json.dumps({
            "message": message,
            "conversationHistory": conversation_history
        }).encode("utf-8")

        # POST リクエストの作成
        req = request.Request(
            FASTAPI_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        # FastAPI エンドポイントへリクエスト
        with request.urlopen(req) as res:
            res_body = res.read().decode("utf-8")
            data = json.loads(res_body)

        # FastAPI からの応答をそのまま返却
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": data.get('reply'),
                "conversationHistory": data.get('conversationHistory', [])
            })
        }

    except Exception as error:
        print("Error calling FastAPI:", error)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }
      