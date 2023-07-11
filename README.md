# Introduction

因近期越南發生多個白牌站點反應網站出現憑證錯誤訊息，以及某些網站訪問出現越南的政府警告頁面，經過排查的結果為部分的 DNS Resolver 被強制更改解析 (DNS劫持)，目前提供了一個小工具讓OP同仁可以進行查詢，以下為工具介紹


# 安裝相依套件

```
git clone https://gitlab.nexiosoft.com/it/tools.git
cd tools/dns-record-check
pip install -r requirements.txt
```


# 使用

## 更改 DNS Server List
目前程式只有抓取越南地區的DNS Server List ，其他地區可以進入 https://public-dns.info/ ，選擇最下方的國家代碼，進入頁面後選取JSON
接著在 main.py 中將 get_public_nameserver_list()函數的requests.get方法內的鏈接更換，未來會使用配置檔方式，目前暫時使用人工寫死在程式裡面。

## 驗證domain的清單檔案
domains.txt內存放要進行驗證的域名列表，每個域名使用換行區隔