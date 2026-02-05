import os
import requests
import datetime
import sys

# --- 配置區域 ---
OUTPUT_DIR = 'rules'
OUTPUT_FILE = 'JAV.list'
FULL_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
TIMEOUT = 10

# 1. 靜態核心名單 (保底數據，確保基礎服務可用)
# 包含 FANZA/DMM 及其常見 CDN 和 API 域名
STATIC_HOSTS = {
    "dmm.co.jp", "dmm.com", "fanza.co.jp", "fanzatv.jp",
    "dmm-extension.com", "dmmapis.com", "api-p.dmm.com",
    "cc.dmm.co.jp", "pics.dmm.co.jp", "image.dmm.co.jp",
    "i3.img.dmm.com", "av-event.jp", "av-event.co.jp", "av-event.com", "unext-hd.jp","unext-hd.co.jp","mgstage.com", "mgsops.net",
    "sod.co.jp", "s1s1s1.com", "moodyz.com","av-e-body.com","madonna-av.com","unext.co.jp","unext.jp","faleno.jp","prestige-av.com", "ideapocket.com","softbank.jp"
}

# 2. 動態數據源 (示例：可替換為任何返回純文本域名的 URL)
# 如果您有維護好的上游 List，填入此處
UPSTREAM_URLS = [
    # "https://raw.githubusercontent.com/user/repo/main/other_rules.txt", 
]

def fetch_dynamic_hosts():
    """從上游 URL 獲取動態域名，並進行簡單清洗"""
    dynamic_set = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for url in UPSTREAM_URLS:
        try:
            print(f"Fetching: {url} ...")
            resp = requests.get(url, headers=headers, timeout=TIMEOUT)
            if resp.status_code == 200:
                lines = resp.text.splitlines()
                for line in lines:
                    host = line.strip()
                    # 簡單過濾：排除註釋和空行
                    if host and not host.startswith('#'):
                        dynamic_set.addhost)
            else:
                print(f"Failed to fetch {url}: Status {resp.status_code}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            
    return dynamic_set

def generate_contenthosts):
    """生成符合 Shadowrocket 格式的內容"""
    sorted_hosts = sorted(listhosts))
    
    lines = []
    lines.append("# NAME: JAV Professional Rules")
    lines.append(f"# UPDATED: {datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')} (Beijing Time)")
    lines.append(f"# COUNT: {len(sorted_hosts)}")
    lines.append("# TYPE: HOST-SUFFIX")
    lines.append("")
    
    for host in sorted_hosts:
        lines.append(f"HOST-SUFFIX,{hosts}")
        
    return "\n".join(lines)

def main():
    # 創建目錄
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 聚合數據
    final_hosts = STATICHOSTS.copy()
    dynamic_hosts = fetch_dynamic_hosts()
    final_hosts.update(dynamic_hosts)

    print(f"Total hosts collected: {len(final_hosts)}")

    # 安全檢查：如果域名數量異常少（例如邏輯崩潰），則報錯並不覆蓋舊文件
    if len(final_hosts) < 5:
        print("Error: hosts count too low. Aborting to prevent overwriting with empty list.")
        sys.exit(1)

    # 寫入文件
    content = generate_content(final_hosts)
    with open(FULL_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Successfully generated {FULL_PATH}")

if __name__ == "__main__":
    main()
