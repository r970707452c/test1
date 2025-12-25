import os
import json
import types
from datetime import datetime, timedelta
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ssl.v20191205 import ssl_client, models
def get_expiring_certificates(days=7):
    try:
        now = datetime.now()
        # 密钥信息从环境变量读取，需要提前在环境变量中设置 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential(os.getenv("TENCENTCLOUD_SECRET_ID"), os.getenv("TENCENTCLOUD_SECRET_KEY"))
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ssl.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ssl_client.SslClient(cred, "", clientProfile)
        listreq = models.DescribeCertificatesRequest()
        params = {

        }
        listreq.from_json_string(json.dumps(params))

        # 返回的resp是一个DescribeCertificatesResponse的实例，与请求对象对应
        listresp = client.DescribeCertificates(listreq)
        # 输出json格式的字符串回包
        #print(listresp.to_json_string())
        #print(listresp)
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
            if cert. get('StatusName') == '证书已颁发'
        ]
    
        # 计算7天后的时间
        seven_days_later = now + timedelta(days=days)

        # 筛选即将过期的证书（过期时间在7天内）
        expiring_soon_certs = []
        expiring_soon_domain = []
        healthy_domain = []
        healthy_certs = []
        for cert in issued_certs:
            # 将证书过期时间字符串转换为datetime对象
            cert_end_time = datetime.strptime(cert['CertEndTime'], '%Y-%m-%d %H:%M:%S')
    
            # 判断是否在7天内过期
            if cert_end_time <= seven_days_later and cert_end_time > now:
                expiring_soon_certs.append(cert['CertificateId'])
                expiring_soon_domain.append(cert['Domain'])
                print(f"证书 {cert['CertificateId']} 将在 {cert['CertEndTime']} 过期（{cert['Domain']}）")
            if cert_end_time >= seven_days_later and cert_end_time > now:
                healthy_certs.append(cert['CertificateId'])
                healthy_domain.append(cert['Domain'])
                print(f"证书 {cert['CertificateId']} 将在 {cert['CertEndTime']} 过期（{cert['Domain']}）")
            for expiring_certs in expiring_soon_domain:
                if expiring_certs in healthy_domain:
                    expiring_soon_domain.remove(cert['Domain'])
                    expiring_soon_certs.remove(cert['CertificateId'])

        print(f"\n7天内即将过期的证书数量: {len(expiring_soon_certs)}")
        print("即将过期证书ID列表:", expiring_soon_certs)
        print("即将过期证书域名列表:", expiring_soon_domain)
        print("正常证书ID列表:", healthy_certs)
        print("正常证书域名列表:", healthy_domain)
        #print(json.dumps(issued_certs, ensure_ascii=False, indent=2))
        return expiring_soon_domain
    except TencentCloudSDKException as err:
        print(err)
if __name__ == "__main__":
    print("即将过期的证书:")
    print(get_expiring_certificates(days=7))
