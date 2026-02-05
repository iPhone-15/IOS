import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

# 目標 URL：這裡是維基百科的日本AV片商列表（示例，可更換為其他聚合站）
TARGET_URL = "https://ja.wikipedia.org/wiki/%E3%82%A2%E3%83%80%E3%83%AB%E3%83%88%E3%83%93%E3%83%87%E3%82%AA%E3%83%A1%E3%83%BC%E3%82%AB%E3%83%BC%E4%B8%80%E8%A6%A7"

# 偽裝成瀏覽器
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_domains():
    try:
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    domains = set()

    # 針對維基百科表格中的外部連結進行提取
    # 注意：具體 Selector 需根據目標網站結構調整
    # 這裡假設提取主要內容區的所有外部連結
    content_div = soup.find('div', {'id': 'bodyContent'})
    
    if not content_div:
        return []

    for link in content_div.find_all('a', href=True):
        href = link['href']
        
        # 過濾非 http 開頭的內部連結
        if not href.startswith('http'):
            continue
            
        # 排除維基百科自身和其他無關域名
        if 'wikipedia.org' in href or 'archive.org' in href:
            continue

        # 提取主域名
        parsed_uri = urlparse(href)
        domain = parsed_uri.netloc
        
        # 移除 www. 前綴以保持簡潔
        if domain.startswith('www.'):
            domain = domain[4:]
            
        if domain:
            domains.add(domain)

    return sorted(list(domains))

def generate_qx_file(domain_list):
    header = [
        "; Summary: Auto-generated Japanese Adult Video Manufacturer Domains",
        "; Compatible with QuantumultX",
        "; Update Frequency: Weekly",
        ""
    ]
    
    # 策略偏好：可預設為 PROXY 或 DIRECT，使用者可在 QX 中覆蓋
    # 格式：HOST-SUFFIX, domain.com, Tag
    rules = [f"HOST-SUFFIX,{d},Japan_Media" for d in domain_list]
    
    content = "\n".join(header + rules)
    
    with open("jav_manufacturers.list", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully generated {len(domain_list)} rules.")

if __name__ == "__main__":
    print("Starting scraper...")
    domains = get_domains()
    if domains:
        generate_qx_file(domains)
    else:
        print("No domains found.")
