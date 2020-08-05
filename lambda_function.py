"""Eats up empty content. Relentless."""
import os
import logging
from datetime import datetime, timedelta
import boto3
from boto3.dynamodb.conditions import Key #, Attr

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# DynamoDB connection
DYNAMODB_RESOURCE = boto3.resource('dynamodb')

# Env
STREAM_TABLE_NAME = os.environ['STREAM_TABLE_NAME']
STREAM_TABLE_IS_SEALED_START_TIME_INDEX_NAME = os.environ[
    'STREAM_TABLE_IS_SEALED_START_TIME_INDEX_NAME']

# CONSTANTS
STREAM_TABLE_IS_SEALED_FIELD = 'isSealed'
STREAM_TABLE_START_TIME_FIELD = 'startTime'
TIME_TO_DELETE = 3 * 86400 # 3 days in seconds

def lambda_handler(event, context):
    """"Default Handler"""
    LOGGER.debug(
        'Content cleansing triggered with event %s', event)

    steram_table = DYNAMODB_RESOURCE.Table(STREAM_TABLE_NAME)
    start_time_old_limit_iso = (datetime.utcnow() - timedelta(seconds=TIME_TO_DELETE)).isoformat()

    query_res = steram_table.query(
        IndexName=STREAM_TABLE_IS_SEALED_START_TIME_INDEX_NAME,
        KeyConditionExpression=Key(STREAM_TABLE_IS_SEALED_FIELD).eq(0) & Key(
            STREAM_TABLE_START_TIME_FIELD).lt(start_time_old_limit_iso),
        Select='ALL_ATTRIBUTES',
        ScanIndexForward=True
    )

    # TODO: Cleanse data
    return query_res.get('Items')
