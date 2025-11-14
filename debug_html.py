#!/usr/bin/env python3
"""
Script để debug HTML - so sánh View Source vs BeautifulSoup
"""
import requests
from bs4 import BeautifulSoup

url = input("Nhập URL cần kiểm tra: ")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
}

response = requests.get(url, headers=headers, timeout=30)
html = response.text

print("=" * 80)
print("HTML mà BeautifulSoup nhận được:")
print("=" * 80)

# Lưu ra file để xem
with open("soup_received.html", "w", encoding="utf-8") as f:
    f.write(html)
print("✅ Đã lưu vào file: soup_received.html")

# Kiểm tra #primary-nav
soup = BeautifulSoup(html, 'html.parser')
nav = soup.select_one("#primary-nav")

if nav:
    print(f"✅ Tìm thấy #primary-nav với {len(nav.select('li'))} thẻ <li>")
else:
    print("❌ KHÔNG tìm thấy #primary-nav")
    print("\nKiểm tra xem có script tags không:")
    scripts = soup.find_all("script")
    print(f"   Số lượng <script> tags: {len(scripts)}")
    
    # Kiểm tra xem có React/Vue/Angular không
    html_lower = html.lower()
    if "react" in html_lower or "reactdom" in html_lower:
        print("   ⚠️  Phát hiện REACT - cần dùng Selenium!")
    if "vue" in html_lower:
        print("   ⚠️  Phát hiện VUE - cần dùng Selenium!")
    if "angular" in html_lower or "ng-app" in html_lower:
        print("   ⚠️  Phát hiện ANGULAR - cần dùng Selenium!")
    
print("\n📝 Hướng dẫn:")
print("1. Mở file soup_received.html")
print("2. So sánh với 'View Source' (Ctrl+U) trên browser")
print("3. Nếu giống nhau → Website dùng JavaScript render")
print("4. Nếu khác nhau → Có thể do cookies, session, hoặc anti-bot")

