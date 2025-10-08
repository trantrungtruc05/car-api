import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
import time
from urllib.parse import urljoin, urlparse

class CategoryCrawler:
    def __init__(self, base_url: str = None):
        """
        Khởi tạo crawler với base URL
        Ví dụ: https://example-car-website.com
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def crawl_categories_from_sample_site(self) -> List[Dict[str, str]]:
        """
        Ví dụ crawl categories từ một trang web mẫu
        Trong thực tế, bạn sẽ thay đổi logic này theo cấu trúc của trang web cụ thể
        """
        categories = []
        
        # Ví dụ crawl từ trang web ô tô (giả định)
        sample_categories = [
            {
                "name": "Xe Sedan",
                "code": "sedan",
                "link": "https://example-car-site.com/sedan"
            },
            {
                "name": "Xe SUV", 
                "code": "suv",
                "link": "https://example-car-site.com/suv"
            },
            {
                "name": "Xe Hatchback",
                "code": "hatchback", 
                "link": "https://example-car-site.com/hatchback"
            },
            {
                "name": "Xe Pickup",
                "code": "pickup",
                "link": "https://example-car-site.com/pickup"
            }
        ]
        
        return sample_categories
    
    def crawl_categories_from_real_site(self, url: str) -> List[Dict[str, str]]:
        """
        Crawl categories từ trang web thực tế
        Ví dụ này sẽ crawl từ một trang web cụ thể
        """
        categories = []
        
        try:
            # Gửi request đến trang web
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Ví dụ: tìm tất cả các link categories
            # Thay đổi selector này theo cấu trúc HTML của trang web bạn muốn crawl
            category_links = soup.find_all('a', class_='category-link')  # Thay đổi class này
            
            for link in category_links:
                # Lấy tên category
                name = link.get_text(strip=True)
                
                # Lấy URL
                href = link.get('href', '')
                full_url = urljoin(url, href) if href else ''
                
                # Tạo code từ name (loại bỏ ký tự đặc biệt, chuyển thành lowercase)
                code = self._generate_code_from_name(name)
                
                if name and code:
                    categories.append({
                        "name": name,
                        "code": code,
                        "link": full_url
                    })
            
            # Thêm delay để tránh bị block
            time.sleep(1)
            
        except requests.RequestException as e:
            print(f"Lỗi khi crawl từ {url}: {str(e)}")
        except Exception as e:
            print(f"Lỗi không xác định: {str(e)}")
        
        return categories
    
    def crawl_categories_from_multiple_pages(self, urls: List[str]) -> List[Dict[str, str]]:
        """
        Crawl categories từ nhiều trang
        """
        all_categories = []
        
        for url in urls:
            print(f"Đang crawl từ: {url}")
            categories = self.crawl_categories_from_real_site(url)
            all_categories.extend(categories)
            
            # Delay giữa các request
            time.sleep(2)
        
        # Loại bỏ duplicate dựa trên code
        unique_categories = []
        seen_codes = set()
        
        for category in all_categories:
            if category['code'] not in seen_codes:
                unique_categories.append(category)
                seen_codes.add(category['code'])
        
        return unique_categories
    
    def _generate_code_from_name(self, name: str) -> str:
        """
        Tạo code từ tên category
        """
        if not name:
            return ""
        
        # Chuyển về lowercase và loại bỏ ký tự đặc biệt
        code = re.sub(r'[^a-zA-Z0-9\s]', '', name.lower())
        # Thay thế khoảng trắng bằng dấu gạch ngang
        code = re.sub(r'\s+', '-', code.strip())
        
        return code
    
    def crawl_categories_from_otosaigon(self) -> List[Dict[str, str]]:
        """
        Ví dụ cụ thể: crawl từ trang web oto Sài Gòn (giả định)
        """
        categories = []
        
        try:
            url = "https://otosaigon.com/mua-ban-xe"  # URL giả định
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Giả định cấu trúc HTML có dạng:
            # <div class="car-categories">
            #   <a href="/sedan" class="category-item">Xe Sedan</a>
            #   <a href="/suv" class="category-item">Xe SUV</a>
            # </div>
            
            category_container = soup.find('div', class_='car-categories')
            if category_container:
                category_items = category_container.find_all('a', class_='category-item')
                
                for item in category_items:
                    name = item.get_text(strip=True)
                    href = item.get('href', '')
                    
                    if name and href:
                        categories.append({
                            "name": name,
                            "code": self._generate_code_from_name(name),
                            "link": urljoin(url, href)
                        })
            
        except Exception as e:
            print(f"Lỗi khi crawl từ otosaigon: {str(e)}")
            # Trả về dữ liệu mẫu nếu crawl thất bại
            categories = self.crawl_categories_from_sample_site()
        
        return categories

# Tạo instance để sử dụng
category_crawler = CategoryCrawler()
