# tencent-ssl-manager（腾讯云免费 SSL 证书自动续期 / FILE 认证）

基于 **腾讯云 SSL Python SDK** 实现的自动化脚本：

- 监控账号下已颁发证书的到期时间
- 在到期前 N 天（默认 7 天/可配置）自动申请新的 **免费 DV 证书**
- 使用 **FILE 认证**（域名验证文件）
- 申请后自动拉取 FILE 验证信息（文件路径/文件名/内容），并执行验证与签发流程轮询）



---

## 目录结构

- `main.py`  
  主入口：获取即将过期的域名 -> 申请新证书 -> 获取 FILE 验证信息 -> 部署验证文件 -> 提交验证 -> 轮询签发结果
- `query_expiring_cert.py`  
  拉取证书列表并筛选即将过期证书（默认 7 天内），返回即将过期的 **域名列表**
- `apply_cert.py`  
  申请免费证书（`ApplyCertificate`，`DvAuthMethod=FILE`），返回 `CertificateId`
- `query_apply_cert.py`  
  根据 `CertificateId` 获取 FILE 验证信息（`DescribeCertificate`），提取：
  - `DvAuthDetail.DvAuthValue`：验证内容
  - `DvAuthDetail.DvAuthKey`：文件名
  - `DvAuthDetail.DvAuthPath`：文件路径
- `check_cert.py`  
  - `complete_cert(certid)`：调用 `CompleteCertificate` 提交验证
  - `check(certid)`：调用 `CheckCertificateDomainVerification` 检查是否已签发（返回 `Issued`）
- `upload_authfile.py`  
  将验证文件上传至 COS（`put_object`）
- `config.py`  
  域名与桶的映射关系：`domain_bucket_list`
- `requirements.txt`  
  依赖：`tencentcloud-sdk-python`、`cos-python-sdk-v5`

---

## 运行前准备

### 1) Python 环境

建议 Python 3.9+：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) 配置腾讯云密钥（环境变量）

脚本从环境变量读取密钥：

- `TENCENTCLOUD_SECRET_ID`
- `TENCENTCLOUD_SECRET_KEY`

示例：

```bash
export TENCENTCLOUD_SECRET_ID="AKIDxxxxxxxxxxxxxxxx"
export TENCENTCLOUD_SECRET_KEY="xxxxxxxxxxxxxxxxxxxx"
```

> 建议使用子账号并配置最小权限（见下文“权限建议”）。

### 3) 配置域名与 COS Bucket 映射

编辑 `config.py`：

```python
domain_bucket_list = [
    {'domain': 'xxx', 'bucket': 'xxx'},
    {'domain': 'xxx', 'bucket': 'xxx'}
]
```


---

## 使用方法

### 1) 手动查看 7 天内即将过期证书

```bash
python query_expiring_cert.py
```

你也可以修改天数（例如 15 天）：

```bash
python -c "from query_expiring_cert import get_expiring_certificates; print(get_expiring_certificates(days=15))"
```

### 2) 执行自动续期流程

```bash
python main.py
```

