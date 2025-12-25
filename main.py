"""Main entry point for SSL certificate renewal automation."""

import json
import time

from apply_cert import apply_cert
from check_cert import check, complete_cert
from config import domain_bucket_list
from deploy_cert import deploy_cdn, deploy_cos
from query_apply_cert import get_apply_cert, refresh_url
from query_expiring_cert import get_expiring_certificates
from upload_authfile import upload

expiring_certs = get_expiring_certificates()

# 申请即将过期的免费证书
if expiring_certs:
    for i in expiring_certs:
        if i not in ["keycloak.aubo-robotics.cn",
                     "download.aubo-robotics.cn"]:
            certid = apply_cert(domain=i)
            dvauthinfo = get_apply_cert(certid=certid)
            dvauthinfo_json = json.loads(dvauthinfo)
            filename = dvauthinfo_json["filename"]
            filepath = dvauthinfo_json["filepath"]
            value = dvauthinfo_json["value"]
            for item in domain_bucket_list:
                if i == item['domain']:
                    upload(
                        filename=filename,
                        filepath=filepath,
                        value=value,
                        bucket=item['bucket']
                    )
                    while True:
                        complete_cert(certid=certid)
                        cert_status = check(certid)
                        print(cert_status)
                        if cert_status:
                            break
                        time.sleep(10)
                        if item['type'] == "cdn":
                            refresh_url(
                                domain=i,
                                filepath=filepath,
                                filename=filename
                            )
                    if item['type'] == "cdn":
                        deploy_cdn(certid=certid, domain=i)
                    elif item['type'] == "cos":
                        deploy_cos(
                            region=item['region'],
                            certid=certid,
                            domain=i,
                            bucket=item['bucket']
                        )

else:
    print("没有即将过期的证书")
