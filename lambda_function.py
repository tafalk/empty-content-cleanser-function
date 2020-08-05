"""Eats up empty content. Relentless."""
import os
import logging
from datetime import datetime, timedelta
import boto3

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# DynamoDB connection
DYNAMODB_RESOURCE = boto3.resource('dynamodb')

# Env
STREAM_TABLE_NAME = os.environ['STREAM_TABLE_NAME']
STREAM_TABLE_IS_SEALED_START_TIME_INDEX_NAME = os.environ[
    'STREAM_TABLE_IS_SEALED_START_TIME_INDEX_NAME']

# CONSTANTS
STREAM_TABLE_BODY_FIELD = 'body'
STREAM_TABLE_IS_SEALED_FIELD = 'isSealed'
STREAM_TABLE_START_TIME_FIELD = 'startTime'
TIME_TO_DELETE = 3 * 86400 # 3 days in seconds

def lambda_handler(event, _context):
    """"Default Handler"""
    LOGGER.debug(
        'Content cleansing triggered with event %s', event)

    deletion_result = []
    stream_table = DYNAMODB_RESOURCE.Table(STREAM_TABLE_NAME)
    start_time_old_limit_iso = (datetime.utcnow() - timedelta(seconds=TIME_TO_DELETE)).isoformat()

    # batch_writer to delete multiple items
    scan_result = stream_table.scan()
    with stream_table.batch_writer() as batch:
        for item in scan_result.get('Items'):
            if (
                    not item.get(STREAM_TABLE_BODY_FIELD)
                    and item.get(STREAM_TABLE_IS_SEALED_FIELD, 0) == 0
                    and item.get(STREAM_TABLE_START_TIME_FIELD) < start_time_old_limit_iso
            ):
                deletion_result.append(item['id'])
                batch.delete_item(
                    Key={
                        'id': item['id']
                    }
                )

    LOGGER.info('Items deleted: %s', deletion_result)
