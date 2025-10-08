#!/usr/bin/env python3
"""
Ví dụ sử dụng API crawl categories
"""
import requests
import json

# Base URL của API
BASE_URL = "http://localhost:8000/api/v1/categories"

def test_crawl_sample_data():
    """Test crawl dữ liệu mẫu"""
    print("=== Test crawl dữ liệu mẫu ===")
    
    response = requests.post(f"{BASE_URL}/crawl-and-import?source=sample")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Thành công: {data['message']}")
        print(f"📊 Tổng tìm thấy: {data['total_found']}")
        print(f"➕ Đã import: {data['imported_count']}")
        print(f"⏭️ Bỏ qua: {data['skipped_count']}")
        print("📋 Categories đã import:")
        for cat in data['categories']:
            print(f"   - {cat['name']} ({cat['code']})")
    else:
        print(f"❌ Lỗi: {response.status_code} - {response.text}")

def test_preview_crawl():
    """Test xem trước dữ liệu crawl"""
    print("\n=== Test preview dữ liệu crawl ===")
    
    response = requests.get(f"{BASE_URL}/crawl-preview?source=sample")
    
    if response.status_code == 200:
        data = response.json()
        print(f"📊 Nguồn: {data['source']}")
        print(f"📊 Tổng categories: {data['total_categories']}")
        print("📋 Dữ liệu sẽ crawl:")
        for cat in data['categories']:
            print(f"   - {cat['name']} ({cat['code']}) - {cat['link']}")
    else:
        print(f"❌ Lỗi: {response.status_code} - {response.text}")

def test_crawl_from_url():
    """Test crawl từ URL cụ thể"""
    print("\n=== Test crawl từ URL cụ thể ===")
    
    # Thay thế bằng URL thực tế
    test_url = "https://example.com/categories"
    
    response = requests.post(f"{BASE_URL}/crawl-and-import?source={test_url}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Thành công: {data['message']}")
        print(f"📊 Nguồn: {data['source']}")
        print(f"📊 Import: {data['imported_count']} categories")
    else:
        print(f"❌ Lỗi: {response.status_code} - {response.text}")

def test_get_all_categories():
    """Test lấy tất cả categories"""
    print("\n=== Test lấy tất cả categories ===")
    
    response = requests.get(f"{BASE_URL}/")
    
    if response.status_code == 200:
        categories = response.json()
        print(f"📊 Tổng categories trong DB: {len(categories)}")
        for cat in categories:
            print(f"   - {cat['name']} ({cat['code']}) - {cat['link']}")
    else:
        print(f"❌ Lỗi: {response.status_code} - {response.text}")

def test_search_categories():
    """Test tìm kiếm categories"""
    print("\n=== Test tìm kiếm categories ===")
    
    search_term = "sedan"
    response = requests.get(f"{BASE_URL}/?search={search_term}")
    
    if response.status_code == 200:
        categories = response.json()
        print(f"🔍 Tìm kiếm '{search_term}': {len(categories)} kết quả")
        for cat in categories:
            print(f"   - {cat['name']} ({cat['code']})")
    else:
        print(f"❌ Lỗi: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("🚀 Bắt đầu test API crawl categories")
    print("📝 Đảm bảo server đang chạy trên http://localhost:8000")
    print("-" * 50)
    
    try:
        # Test preview trước
        test_preview_crawl()
        
        # Test crawl và import
        test_crawl_sample_data()
        
        # Test lấy tất cả
        test_get_all_categories()
        
        # Test tìm kiếm
        test_search_categories()
        
        # Test crawl từ URL (nếu có URL thực)
        # test_crawl_from_url()
        
    except requests.exceptions.ConnectionError:
        print("❌ Không thể kết nối đến server. Hãy chắc chắn server đang chạy!")
    except Exception as e:
        print(f"❌ Lỗi không xác định: {e}")
    
    print("\n✅ Hoàn thành test!")
