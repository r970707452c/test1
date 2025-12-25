#!/bin/python

import os
import json
import types
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ssl.v20191205 import ssl_client, models
from tencentcloud.cdn.v20180606 import cdn_client, models
def get_apply_cert(certid):
    try:
    # 密钥信息从环境变量读取，需要提前在环境变量中设置 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY
        cred = credential.Credential(os.getenv("TENCENTCLOUD_SECRET_ID"), os.getenv("TENCENTCLOUD_SECRET_KEY"))
    # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ssl.tencentcloudapi.com"
    #    certid = certid

    # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
    # 实例化要请求产品的client对象,clientProfile是可选的
        client = ssl_client.SslClient(cred, "", clientProfile)
    # 实例化一个请求对象,每个接口都会对应一个request对象
        queryreq = models.DescribeCertificateRequest()
        params = {
            "CertificateId": certid
        }
        queryreq.from_json_string(json.dumps(params))

    # 返回的resp是一个DescribeCertificateResponse的实例，与请求对象对应
        queryresp = client.DescribeCertificate(queryreq)
    # 输出json格式的字符串回包
        #print(resp.to_json_string())
        #print(queryresp.DvAuthDetail.DvAuthValue)
        content=(queryresp.DvAuthDetail.DvAuthValue)
        filename=(queryresp.DvAuthDetail.DvAuthKey)
        filepath=(queryresp.DvAuthDetail.DvAuthPath)
        data = {
            "value": content,
            "filename": filename,
            "filepath": filepath
        }
        data_json = json.dumps(data, ensure_ascii=False, indent=2)
        #print(data_json)
        return data_json
    except TencentCloudSDKException as err:
        print(err)
def refresh_url(domain,filepath,filename):
    try:
        cred = credential.Credential(os.getenv("TENCENTCLOUD_SECRET_ID"), os.getenv("TENCENTCLOUD_SECRET_KEY"))
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cdn.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = cdn_client.CdnClient(cred, "", clientProfile)
        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.PurgeUrlsCacheRequest()
        params = {
            ["https://"+domain+filepath+filename]
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个PurgeUrlsCacheResponse的实例，与请求对象对应
        resp = client.PurgeUrlsCache(req)
        # 输出json格式的字符串回包
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)
if __name__ == "__main__":
    print("即将过期的证书:")
    print(get_apply_cert())
