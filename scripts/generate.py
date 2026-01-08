import os
import datetime
import pytz
import requests

# 上游数据源：v2fly 社区维护的 konami 列表
UPSTREAM_URL = "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/konami"

def get_local_domains():
    """
    本地强制包含的域名列表（用于补充社区列表可能缺失的 Master Duel 专用域名）
    """
    return [
        "konami-md.jp",
        "md-game.konami.net",
        "md-info.konami.net",
        "p.eagate.573.jp",
        "duellinks.konami.net",
        "yugioh-card.com",
        "konami.net"
    ]

def fetch_upstream_domains():
    """
    从 v2fly 社区获取最新的 konami 域名列表
    """
    print(f"正在从上游抓取数据: {UPSTREAM_URL} ...")
    domains = set()
    try:
        response = requests.get(UPSTREAM_URL, timeout=10)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        for line in lines:
            line = line.strip()
            # 忽略注释和空行，忽略 include 指令（通常 konami 列表没有 include）
            if not line or line.startswith("#") or line.startswith("include:"):
                continue
            
            # v2fly 格式通常直接是域名，有时包含 attributes 如 @ads，需要去除
            domain = line.split()[0]
            domains.add(domain)
            
        print(f"成功获取上游域名 {len(domains)} 个")
    except Exception as e:
        print(f"⚠️ 上游抓取失败，将仅使用本地列表。错误信息: {e}")
    
    return domains

def generate_shadowrocket_rule():
    output_dir = "rules"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = os.path.join(output_dir, "konami.list")

    # 1. 获取本地列表
    final_domains = set(get_local_domains())
    
    # 2. 获取远程列表并合并
    remote_domains = fetch_upstream_domains()
    final_domains.update(remote_domains)
    
    # 3. 排序以便阅读
    sorted_domains = sorted(list(final_domains))

    # 4. 准备文件内容
    tz = pytz.timezone('Asia/Shanghai')
    now = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    
    content = []
    content.append(f"# Konami & Master Duel Rules for Shadowrocket")
    content.append(f"# Updated: {now} (Beijing Time)")
    content.append(f"# Source: Local + v2fly/domain-list-community")
    content.append(f"# Total Domains: {len(sorted_domains)}")
    content.append("")
    
    # 5. 写入规则 (默认为 DOMAIN-SUFFIX)
    for domain in sorted_domains:
        content.append(f"DOMAIN-SUFFIX,{domain}")
        
    # 补充关键词
    content.append("DOMAIN-KEYWORD,masterduel")
    content.append("DOMAIN-KEYWORD,yugioh")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("\n".join(content))
        
    print(f"✅ 规则文件已生成: {filename} (共 {len(sorted_domains)} 条域名)")

if __name__ == "__main__":
    generate_shadowrocket_rule()
