import requests
import re

def get_domains():
    # 1. 預定義的核心域名 (確保基本盤穩定)
    core_domains = {
        "prestige-av.com", "p-m-g.jp","hnext.jp","unext.jp", "p-av.com", "dmm.co.jp", "dmm.com", 
        "fanza.jp", "mgstage.com","faleno.jp"}
# 2. 嘗試從社群維護的精選列表抓取更多（可選，增加擴展性）
    # 這裡抓取著名的 ACL4SSR 日本媒體清單作為補強
    extra_domains = set()
    try:
        url = "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/JapanMedia.list"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            # 提取包含關鍵字的行
            keywords = ['prestige', 'dmm', 'fanza', 'will-inc']
            for line in res.text.splitlines():
                if any(k in line.lower() for k in keywords) and "DOMAIN" in line:
                    domain = line.split(',')[1].strip()
                    extra_domains.add(domain)
    except:
        print("遠端抓取失敗，將使用核心清單。")

    all_domains = core_domains.union(extra_domains)
    return sorted(list(all_rules_format(all_domains)))

def all_rules_format(domain_list):
    rules = []
    for d in domain_list:
        if d: rules.append(f"DOMAIN-SUFFIX,{d}")
    return rules

if __name__ == "__main__":
    final_list = get_domains()
    with open("JAV_DOMAIN.list", "w", encoding="utf-8") as f:
        f.write("# JAV DOMAIN Ruleset - Auto Updated\n")
        f.write("# Included: Prestige, DMM, FANZA,Hnext,Unext, etc.\n")
        f.write("\n".join(final_list))
    print(f"成功生成 {len(final_list)} 條規則")
