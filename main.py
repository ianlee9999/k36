import logging
import requests

from dns import resolver, exception
from prettytable import PrettyTable
from concurrent.futures import ThreadPoolExecutor, as_completed


def init_logging():
    global logger
    logger = logging.getLogger()  
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    fh = logging.FileHandler("logs/dns_record_check.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    
    logger.addHandler(ch)
    logger.addHandler(fh)

def init_prettytable():
    global tb1 

    logger.debug("初始化及設置PrettyTalbe相關屬性")
    tb1 = PrettyTable()
    tb1.field_names = ["organization", "nameserver", "domain", "record"]
    tb1.sortby = "organization"
    tb1.align["organization"] = "l"
    tb1.align["nameserver"] = "l"
    tb1.align["domain"] = "l"
    tb1.align["record"] = "l"

def get_public_nameserver_list():
    """
    取得在越南地區常用的DNS列表
    """

    content = requests.get("https://public-dns.info/nameserver/vn.json").json()

    # pop出不必要使用的欄位
    for item in content:
        for key in ['a', 'name', 'as_number', 'version', 'error', 'dnssec', 'reliability', 'checked_at', 'created_at']:
            item.pop(key, None)

    return content

def get_dns_record(nameserver_ip, organization, domain):
    try:
        # DNS初始設定
        dns_resolver = resolver.Resolver()
        dns_resolver.timeout = 3
        dns_resolver.lifetime = 5
        dns_resolver.nameservers = [nameserver_ip]

        # Response JSON
        result = {
            "nameserver": nameserver_ip,
            "organization": organization,
            "domain": domain,
            "record": [],
        }

        # 將結果更新到record
        for response_data in dns_resolver.query(domain):
            result.get("record").append(response_data.address)
        return result

    except resolver.NXDOMAIN:
        result.get("record").append("Non-Existent Domain")
        return result

    except exception.Timeout as e:
        # DNS operation timed out
        result.get("record").append("DNS operation timed out")
        return result

    except Exception as e:
        result.get("record").append("其他異常")
        return result

def main():
    """
    程式進入點
    """

    # 程式初始化
    init_logging()
    init_prettytable()

    logger.debug("準備取得name server列表")
    nameservers_list = get_public_nameserver_list()
    print(nameservers_list)

    # Thread 數量
    THREAD_COUNT = 20
    logger.debug(f"啟動{THREAD_COUNT}個thread去進行解析")

    # 讀檔
    with open("domains.txt", "r") as f:
        # 逐行讀取
        for line in f:
            domain = line.strip("\n")
            logger.debug(f"域名: {domain}")

            # 啟動20個thread去做DNS解析
            with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
                futures = []
                for nameserver in nameservers_list:
                    future = executor.submit(
                        get_dns_record,
                        nameserver.get("ip"),
                        nameserver.get("as_org"),
                        domain,
                    )
                    futures.append(future)

                for future in as_completed(futures):
                    data = future.result()
                    tb1.add_row(
                        [
                            data.get("organization"),
                            data.get("nameserver"),
                            data.get("domain"),
                            data.get("record"),
                        ]
                    )
                logging.info(tb1)
                logging.info("")
                logging.info("")

                # 清空內容，給下一個Domain使用
                tb1.clear_rows()


if __name__ == "__main__":
    main()
