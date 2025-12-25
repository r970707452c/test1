import os
import json
import types
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ssl.v20191205 import ssl_client, models

def complete_cert(certid):
    try:
        cred = credential.Credential(os.getenv("TENCENTCLOUD_SECRET_ID"), os.getenv("TENCENTCLOUD_SECRET_KEY"))

        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ssl.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ssl_client.SslClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.CompleteCertificateRequest()
        params = {
            "CertificateId": certid
        }
        req.from_json_string(json.dumps(params))
    
        # 返回的resp是一个CompleteCertificateResponse的实例，与请求对象对应
        resp = client.CompleteCertificate(req)
        # 输出json格式的字符串回包
        print(resp.to_json_string())
        return resp
    except TencentCloudSDKException as err:
        print(err)
        
def check(certid):
    try:
        cred = credential.Credential(os.getenv("TENCENTCLOUD_SECRET_ID"), os.getenv("TENCENTCLOUD_SECRET_KEY"))

        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ssl.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ssl_client.SslClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.CheckCertificateDomainVerificationRequest()
        params = {
            "CertificateId": certid
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个CheckCertificateDomainVerificationResponse的实例，与请求对象对应
        resp = client.CheckCertificateDomainVerification(req)
        # 输出json格式的字符串回包
        #print(resp.to_json_string())

        return resp.VerificationResults[0].Issued
    except TencentCloudSDKException as err:
        print(err)
