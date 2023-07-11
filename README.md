Table of contents

- [簡介](#簡介)
- [安裝](#安裝)
- [使用](#使用)
  - [更改 DNS Server List](#更改-dns-server-list)
  - [驗證domain的清單檔案](#驗證domain的清單檔案)


# 簡介
因近期發生多個客戶反應網站出現憑證錯誤訊息或是政府警告頁面，經調查發現該地區部分的 DNS Resolver 將域名強制更改解析 (DNS劫持)，目前撰寫了一個小工具讓OP一線同仁可以進行查詢

以下為工具安裝方式

# 安裝

```
# Clone專案
git clone https://github.com/Spencer810704/dns-check-tool

# 切換目錄
cd dns-check-tool

# 安裝套件
pip install -r requirements.txt
```


# 使用

## 更改 DNS Server List
目前程式只有抓取越南地區的DNS Server List ，其他地區可以進入 https://public-dns.info/ ，選擇最下方的國家代碼，進入頁面後選取JSON
接著在 main.py 中將 `get_public_nameserver_list()` 函數的 `requests.get`方法內的鏈接更換，未來會使用配置檔方式，目前暫時使用人工寫死在程式裡面。

## 驗證domain的清單檔案
`domains.txt` 內存放要進行驗證的域名列表，每個域名使用換行區隔