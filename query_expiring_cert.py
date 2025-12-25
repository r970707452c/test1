"""Query and identify expiring SSL certificates."""

import json
import os
from datetime import datetime, timedelta

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import \
    TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ssl.v20191205 import models, ssl_client


def get_expiring_certificates(days=7):
    """
    Get list of certificates expiring within specified days.

    Args:
        days: Number of days to check for expiration (default: 7)

    Returns:
        List of domain names with expiring certificates
    """
    try:
        now = datetime.now()
        # 密钥信息从环境变量读取
        # 需要提前在环境变量中设置 TENCENTCLOUD_SECRET_ID
        # 和 TENCENTCLOUD_SECRET_KEY
        # 密钥可前往官网控制台进行获取
        # https://console.cloud.tencent.com/cam/capi
        cred = credential.Credential(
            os.getenv("TENCENTCLOUD_SECRET_ID"),
            os.getenv("TENCENTCLOUD_SECRET_KEY")
        )
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ssl.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象，clientProfile是可选的
        client = ssl_client.SslClient(cred, "", clientProfile)
        listreq = models.DescribeCertificatesRequest()
        params = {}
        listreq.from_json_string(json.dumps(params))

        # 返回的resp是一个DescribeCertificatesResponse的实例
        # 与请求对象对应
        listresp = client.DescribeCertificates(listreq)
        # 输出json格式的字符串回包
        response_json = listresp.to_json_string()
        data = json.loads(response_json)

        # 检查数据结构
        if 'Certificates' in data:
            # 数据在根层级
            certificates = data['Certificates']
        elif 'Response' in data and 'Certificates' in data['Response']:
            # 数据在Response层级
            certificates = data['Response']['Certificates']
        else:
            print("未找到证书数据:", data)
            certificates = []

        # 筛选已颁发的证书
        issued_certs = [
            {
                'CertificateId': cert['CertificateId'],
                'Domain': cert['Domain'],
                'CertEndTime': cert['CertEndTime'],
                'Status': cert['StatusName']
            }
            for cert in certificates
            if cert.get('StatusName') == '证书已颁发'
        ]

        # 计算N天后的时间
        n_days_later = now + timedelta(days=days)

        # 筛选即将过期的证书（过期时间在N天内）
        expiring_soon_certs = []
        expiring_soon_domain = []
        healthy_domain = []
        healthy_certs = []
        for cert in issued_certs:
            # 将证书过期时间字符串转换为datetime对象
            cert_end_time = datetime.strptime(
                cert['CertEndTime'],
                '%Y-%m-%d %H:%M:%S'
            )

            # 判断是否在N天内过期
            if cert_end_time <= n_days_later and cert_end_time > now:
                expiring_soon_certs.append(cert['CertificateId'])
                expiring_soon_domain.append(cert['Domain'])
                print(
                    f"证书 {cert['CertificateId']} 将在 "
                    f"{cert['CertEndTime']} 过期（{cert['Domain']}）"
                )
            if cert_end_time >= n_days_later and cert_end_time > now:
                healthy_certs.append(cert['CertificateId'])
                healthy_domain.append(cert['Domain'])
                print(
                    f"证书 {cert['CertificateId']} 将在 "
                    f"{cert['CertEndTime']} 过期（{cert['Domain']}）"
                )
            for expiring_certs in expiring_soon_domain:
                if expiring_certs in healthy_domain:
                    expiring_soon_domain.remove(cert['Domain'])
                    expiring_soon_certs.remove(cert['CertificateId'])

        print(f"\n{days}天内即将过期的证书数量: {len(expiring_soon_certs)}")
        print("即将过期证书ID列表:", expiring_soon_certs)
        print("即将过期证书域名列表:", expiring_soon_domain)
        print("正常证书ID列表:", healthy_certs)
        print("正常证书域名列表:", healthy_domain)
        return expiring_soon_domain
    except TencentCloudSDKException as err:
        print(err)
        return []


if __name__ == "__main__":
    print("即将过期的证书:")
    print(get_expiring_certificates(days=7))
