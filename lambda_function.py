"""Resource Searcher"""
import os
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def lambda_handler(event, context):
    """"Default Handler"""
    LOGGER.debug(
        'Content cleansing triggered with event %s', event)

    # DynamoDB connection and tables
    dynamodb = boto3.resource('dynamodb')
    stream_table = dynamodb.Table(os.environ['STREAM_TABLE_NAME'])

    # TODO: Cleanse data
    return
