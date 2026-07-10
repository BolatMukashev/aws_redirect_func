import asyncio
import json
import aiobotocore.session
from config import AWS_QUEUE_URL, AWS_REGION
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


async def send_to_queue(body: str):
    """Публикация апдейта в AWS SQS"""
    session = aiobotocore.session.get_session()
    async with session.create_client("sqs", region_name=AWS_REGION) as client:
        await client.send_message(QueueUrl=AWS_QUEUE_URL, MessageBody=body)


async def async_handler(event, context):
    logger.info(f"EVENT: {event}")

    body_str = event.get("body")
    if not body_str:
        logger.info("Пустое тело запроса, пропускаем")
        return {"statusCode": 200}

    logger.info(f"BODY: {body_str}")
    await send_to_queue(body_str)

    return {"statusCode": 200}


def handler(event, context):
    return asyncio.run(async_handler(event, context))