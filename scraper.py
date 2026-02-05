import requests
import time

def get_jav_domains_from_wikidata():
    # SPARQL 查询语句：
    # 查找所有 (实例是=成人视频制造商) 且 (国家=日本) 的 (官方网站)
    url = 'https://query.wikidata.org/sparql'
    query = """
    SELECT DISTINCT ?website WHERE {
      ?item wdt:P31/wdt:P279* wd:Q2081546 .  # 实例是：成人视频制造商
      ?item wdt:P17 wd:Q17 .                 # 国家是：日本
      ?item wdt:P856 ?website .              # 获取官方网站属性
    }
    """
    
    # Wikidata 要求必须带 User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Python/3.9 QuantumultX-List-Generator',
        'Accept': 'application/json'
    }

    try:
        r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"Wikidata Query Failed: {e}")
        return []

    domains = set()
    
    for item in data['results']['bindings']:
        raw_url = item['website']['value']
        # 简单的域名提取逻辑
        from urllib.parse import urlparse
        parsed = urlparse(raw_url)
        domain = parsed.netloc
        
        # 移除 www.
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # 过滤掉常见的平台域名（如果不想包含 DMM 或 Twitter 等）
        if 'twitter.com' not in domain and 'facebook.com' not in domain:
            domains.add(domain)

    return sorted(list(domains))

def generate_qx_file(domain_list):
    header = [
        "; Summary: JAV Studio Domains from Wikidata",
        "; Total Rules: " + str(len(domain_list)),
        "; Updated: " + time.strftime("%Y-%m-%d"),
        ""
    ]
    rules = [f"HOST-SUFFIX,{d},Japan_Media" for d in domain_list]
    content = "\n".join(header + rules)
    
    with open("jav_manufacturers.list", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Success! Generated {len(domain_list)} domains.")

if __name__ == "__main__":
    print("Querying Wikidata...")
    domains = get_jav_domains_from_wikidata()
    if domains:
        generate_qx_file(domains)
    else:
        print("No domains found.")
