# Hướng dẫn sử dụng tính năng Crawl Categories

## Tổng quan

Thay vì nhập dữ liệu categories từ body request, hệ thống giờ đây có thể tự động crawl dữ liệu từ các trang web và import vào database.

## Các API mới

### 1. Crawl và Import dữ liệu
```
POST /api/v1/categories/crawl-and-import?source={source}
```

**Tham số:**
- `source`: Nguồn dữ liệu
  - `sample`: Dữ liệu mẫu (mặc định)
  - `otosaigon`: Crawl từ trang oto Sài Gòn (ví dụ)
  - URL cụ thể: `https://example.com/categories`

**Response:**
```json
{
  "message": "Đã crawl và import thành công từ sample",
  "source": "sample",
  "total_found": 4,
  "imported_count": 4,
  "skipped_count": 0,
  "categories": [
    {
      "id": 1,
      "name": "Xe Sedan",
      "code": "xe-sedan",
      "link": "https://example-car-site.com/sedan"
    }
  ]
}
```

### 2. Preview dữ liệu trước khi import
```
GET /api/v1/categories/crawl-preview?source={source}
```

**Response:**
```json
{
  "source": "sample",
  "total_categories": 4,
  "categories": [
    {
      "name": "Xe Sedan",
      "code": "xe-sedan",
      "link": "https://example-car-site.com/sedan"
    }
  ]
}
```

### 3. Crawl từ nhiều nguồn
```
POST /api/v1/categories/crawl-multiple?urls=url1&urls=url2
```

## Cách sử dụng

### 1. Crawl dữ liệu mẫu
```bash
curl -X POST "http://localhost:8000/api/v1/categories/crawl-and-import?source=sample"
```

### 2. Preview dữ liệu trước
```bash
curl "http://localhost:8000/api/v1/categories/crawl-preview?source=sample"
```

### 3. Crawl từ URL cụ thể
```bash
curl -X POST "http://localhost:8000/api/v1/categories/crawl-and-import?source=https://example.com/categories"
```

### 4. Sử dụng Python script
```bash
python example_crawl_usage.py
```

## Tùy chỉnh Crawler

### Thêm nguồn crawl mới

1. Mở file `app/services/crawler.py`
2. Thêm method mới trong class `CategoryCrawler`:

```python
def crawl_categories_from_your_site(self) -> List[Dict[str, str]]:
    """Crawl từ trang web của bạn"""
    categories = []
    
    try:
        url = "https://your-website.com/categories"
        response = self.session.get(url, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tùy chỉnh selector theo cấu trúc HTML của trang web
        category_links = soup.find_all('a', class_='your-category-class')
        
        for link in category_links:
            name = link.get_text(strip=True)
            href = link.get('href', '')
            
            categories.append({
                "name": name,
                "code": self._generate_code_from_name(name),
                "link": urljoin(url, href)
            })
            
    except Exception as e:
        print(f"Lỗi: {e}")
        
    return categories
```

3. Cập nhật endpoint để hỗ trợ nguồn mới:

```python
# Trong file app/api/v1/endpoints/categories.py
elif source == "your-site":
    categories_data = category_crawler.crawl_categories_from_your_site()
```

### Tùy chỉnh HTML selector

Thay đổi các selector trong method crawl:

```python
# Ví dụ các selector phổ biến
category_links = soup.find_all('a', class_='category-link')
category_links = soup.select('.categories a')
category_links = soup.find_all('div', {'data-category': True})
```

## Lưu ý

1. **Rate limiting**: Crawler có delay giữa các request để tránh bị block
2. **Duplicate handling**: Hệ thống tự động bỏ qua categories đã tồn tại (theo code)
3. **Error handling**: Nếu crawl thất bại, sẽ fallback về dữ liệu mẫu
4. **Code generation**: Tự động tạo code từ tên category (loại bỏ ký tự đặc biệt)

## Ví dụ thực tế

### Crawl từ trang bán xe

```python
def crawl_categories_from_car_site(self):
    url = "https://banxe.com/danh-muc"
    response = self.session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    categories = []
    for item in soup.select('.category-list .category-item'):
        name = item.find('h3').get_text(strip=True)
        link = item.find('a')['href']
        
        categories.append({
            "name": name,
            "code": self._generate_code_from_name(name),
            "link": urljoin(url, link)
        })
    
    return categories
```

## Troubleshooting

1. **Lỗi kết nối**: Kiểm tra URL và network
2. **Không tìm thấy dữ liệu**: Kiểm tra CSS selector
3. **Duplicate entries**: Categories với cùng code sẽ bị bỏ qua
4. **Timeout**: Tăng timeout trong crawler config
