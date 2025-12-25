#!/bin/python

import os
import json
import types
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ssl.v20191205 import ssl_client, models
def apply_cert(domain):
    try:
        # 密钥信息从环境变量读取，需要提前在环境变量中设置 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY
        cred = credential.Credential(os.getenv("TENCENTCLOUD_SECRET_ID"), os.getenv("TENCENTCLOUD_SECRET_KEY"))
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ssl.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ssl_client.SslClient(cred, "", clientProfile)
        applyreq = models.ApplyCertificateRequest()

        params = {
            "DvAuthMethod": "FILE",
            "DomainName": domain
        }
        applyreq.from_json_string(json.dumps(params))

        # 返回的resp是一个ApplyCertificateResponse的实例，与请求对象对应
        applyresp = client.ApplyCertificate(applyreq)
        # 输出json格式的字符串回包
        #print(applyresp.CertificateId)
        certid=(applyresp.CertificateId)
        return certid
    except TencentCloudSDKException as err:
        print(err)
if __name__ == "__main__":
    print("申请证书成功:")
    print(apply_certificates())


