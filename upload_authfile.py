#!/bin/python
"""Upload authentication file to Tencent Cloud COS."""

import logging
import os
import sys

from qcloud_cos import CosConfig, CosS3Client


def upload(value, filename, filepath, bucket):
    """
    Upload authentication file to COS bucket.

    Args:
        value: File content to upload
        filename: Name of the file
        filepath: Path where file should be stored
        bucket: Target COS bucket name
    """
    # 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG
    # 此时SDK会打印和服务端的通信信息
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # 替换为用户的 SecretId
    # 请登录访问管理控制台进行查看和管理
    # https://console.cloud.tencent.com/cam/capi
    secret_id = os.getenv("TENCENTCLOUD_SECRET_ID")
    # 替换为用户的 SecretKey
    # 请登录访问管理控制台进行查看和管理
    # https://console.cloud.tencent.com/cam/capi
    secret_key = os.getenv("TENCENTCLOUD_SECRET_KEY")
    # 替换为用户的 region
    # 已创建桶归属的region可以在控制台查看
    # https://console.cloud.tencent.com/cos5/bucket
    region = 'ap-beijing'
    # COS支持的所有region列表参见
    # https://cloud.tencent.com/document/product/436/6224
    # 如果使用永久密钥不需要填入token
    # 如果使用临时密钥需要填入，临时密钥生成和使用指引参见
    # https://cloud.tencent.com/document/product/436/14048
    token = None

    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key,
        Token=token
    )
    client = CosS3Client(config)

    client.put_object(
        Bucket=bucket,
        Body=value,
        Key=filepath + filename,
        EnableMD5=False
    )
