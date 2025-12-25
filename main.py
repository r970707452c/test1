import time
import json
from query_expiring_cert import get_expiring_certificates
from apply_cert import apply_cert
from query_apply_cert import get_apply_cert,refresh_url
from upload_authfile import upload
from config import domain_bucket_list
from check_cert import check,complete_cert
from deploy_cert import deploy_cos,deploy_cdn

expiring_certs = get_expiring_certificates()

# 申请即将过期的免费证书
if expiring_certs:
    for i in expiring_certs:
        if i not in ["keycloak.aubo-robotics.cn","download.aubo-robotics.cn"]:
            certid = apply_cert(domain=i)
            dvauthinfo = get_apply_cert(certid=certid)
            dvauthinfo_json = json.loads(dvauthinfo)
            filename=dvauthinfo_json["filename"]
            filepath=dvauthinfo_json["filepath"]
            value=dvauthinfo_json["value"]
            for list in domain_bucket_list:
                if i == list['domain']:
                    upload(filename=filename,filepath=filepath,value=value,bucket=list['bucket'])
                    while True:
                        complete_cert(certid=certid)
                        cert_status = check(certid)
                        print(cert_status)
                        if cert_status:
                            break
                        time.sleep(10)
                        if list['type'] == "cdn":
                           refresh_url(domain=i,filepath=filepath,filename=filepath) 
                    if list['type'] == "cdn":
                        deploy_cdn(certid=certid,domain=i)
                    elif list['type'] == "cos":
                        deploy_cos(region=list['region'],certid=certid,domain=i,bucket=list['bucket'])
            
else: 
    print("没有即将过期的证书")
