from alipay import AliPay
alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwqdG6DlyVk0JEKB34cFYn48WpcqtsGLEbIs8oXJNFstuWLHspAmBnIlrr7ljD8spaj/3Cz0G+493tuC8fiejxc3spHj4z833EYFWlbhu+nenr0aCPBFtq1o7AYpTpXIZjXBf6roHiYTbQjD9Vws3fr5JmVTRNkcHc6/P3Bv4RxP/kjFuLcABximakYsinCJ2vg1SLI+ADdlcfln/9RIqkyrKekck491rpsIeTA2meyCgMTSJExEDMsWDFw+mmYvMPqKVxOFbkitNv1vEdS+Ucm+8i8yzrIapWGpLtavyA2591+BiffCxoZhL+RgFRVxuOzHOn5YZe+EwxJ4YsPWjLwIDAQAB
-----END PUBLIC KEY-----"""

app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAwqdG6DlyVk0JEKB34cFYn48WpcqtsGLEbIs8oXJNFstuWLHspAmBnIlrr7ljD8spaj/3Cz0G+493tuC8fiejxc3spHj4z833EYFWlbhu+nenr0aCPBFtq1o7AYpTpXIZjXBf6roHiYTbQjD9Vws3fr5JmVTRNkcHc6/P3Bv4RxP/kjFuLcABximakYsinCJ2vg1SLI+ADdlcfln/9RIqkyrKekck491rpsIeTA2meyCgMTSJExEDMsWDFw+mmYvMPqKVxOFbkitNv1vEdS+Ucm+8i8yzrIapWGpLtavyA2591+BiffCxoZhL+RgFRVxuOzHOn5YZe+EwxJ4YsPWjLwIDAQABAoIBAGTsznsBriLI9nZEfWP0F7tDOX7kw4G89BNDbkBXP1keSSx7tDKpKya6qbcG7DH4KJUKbVDKZ6BvFqcfhxvx+ZxJ1PTCNF+qbvwIj5g5dHExMSRT7pqufqplskpuKkiSDGWlalYN9nJ7DCQZuoEzM6bnismRjJgT4+07rw51Ahn3gQJ3W3vkhaRbpOP57t7bhZSNuVcv4O99INrlrJeF6pKN5RDOqHjEV6cdi08iApADXZUaJqPOLGkymiZkHf7b5lcv44knWKrWI8xs/8G/9en8BWHPcTPMD5Ml1exdRyDECaTiFd/qKH+fWSCxuwqgl56nBcKQ8ChMbCMenNsvlIECgYEA4FS4Df4ACP5VlLMXd6oh4x99BLfJel3qML0DhrXHInVGCgshlUeXzwOB8MLpqDFKf7kiGD9Wjc7x4nRr/OPBlmkts3a/ma35mX2mRvC0embuqXwaBfrYAI2+aeVMF2mQE36GmXGNjTje6ciNIm+nRYAE3RtokuT42cJEv2kEU5ECgYEA3iIEndlhwc6ZVwbAbmW79IEJSCU8scPWk+7acLW8gXfnhupfUiN7s6KUJZrhYaEnevZH7talNiP6LPApGXW1Mme/PNLyZqe4sNUBMGFgEqWphVna2zv+fiA+yLHSu9j6g3mY/RO9dG9qVTNxseRqng3Jbu2Cwhj3rO23OHrtqr8CgYBv6ROgt1PhKLAc7HMKmW8qVO0TS3RRfUR1Z/W4YDqlcAeuvvrT89FBzqgmKbZS17Qon3zox8AwIkr9A8NTd3N9y56m5tiSm/3mmo422aHPZkYteuGolgjnzc5uGZuqGllrwDT5m3JYP0TFL+1ofnbd7w1+GExE68FRMN8G9ibYYQKBgFmBLYkI+WnlPEYjs1AIcBaSE9JdJrqeJY0QFjaKE/26+bCUKXpoT8TPApCwepYjIExchhmHpaROFNUcpALdOfiocxcoDIIunK2r9kGvSs3YsJjJ3vStlNrvVTz64eXNBQwK6Ak5dgI/joHsK6i5V/h9p6epziE1fD7Svhvk9HTzAoGBALXmpgkHMxqLvH8oIh4E2E9H1l804Nha/vxsSIkh6Ef+h3mcjIAquGKw+nHKfXzohaOnvRj+N15vxPnCvT1WXHUAOYI/exgjZRoswJh9JT/pOOUJkLqAcLqH3L9D+8VswyeGBJzQkHrsVFTe5lAqIRZuO9Hw3AIqXAzuEJHJCbOG
-----END RSA PRIVATE KEY-----"""

#实例化支付应用
alipay = AliPay(
    appid = "2016101000652516",
    app_notify_url = None,
    app_private_key_string = app_private_key_string,
    alipay_public_key_string = alipay_public_key_string,
    sign_type= "RSA2"
)

#发起支付请求
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="33457", #订单号
    total_amount=str(1000.01),#支付金额
    subject="生鲜交易", #交易主题
    return_url=None,
    notify_url=None
)

#发起支付请求
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="33459", #订单号
    total_amount=str(100000000.01),#支付金额
    subject="生鲜交易", #交易主题
    return_url=None,
    notify_url=None
)

print("https://openapi.alipaydev.com/gateway.do?"+order_string)