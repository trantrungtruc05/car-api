from math import e
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from app.core.database import get_db
from app.schemas.car_schema import CarsCreate
from app.crud import cars_crud
import re

BASE_URL = "https://bonbanh.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
}

def start_crawl():

    db = next(get_db())

    total_page = calc_total_page(BASE_URL)
    for page in range(1173, int(total_page)):
        print(BASE_URL + f"oto/page,{page}")
        resp = requests.get(BASE_URL + f"oto/page,{page}", headers=headers, timeout=10)
        resp.raise_for_status()

        html = resp.text
        soup = BeautifulSoup(html, "html.parser")

        
        h_list_car = soup.find('div', id='s-list-car')
        g_box_content = h_list_car.find('div', class_='g-box-content')

        
        
        for content in g_box_content.find_all('li', class_='car-item'):
            name = content.find('a')['href']
            print(urljoin(BASE_URL, name))
            
            # Extract data once to avoid multiple requests
            detail_url = urljoin(BASE_URL, name)
            extended_info = extract_extended_info(detail_url)
            seller_info = extract_seller_info(detail_url)
            general_info = extract_general_info(content)
            
            # insert into cars table
            cars_create = CarsCreate(
                car_id=general_info['car_id'],
                brand = extract_brand(detail_url) or "",
                name=general_info['name'],
                price=general_info['price'],
                location=general_info['location'],
                status=general_info['status'],
                year=general_info['year'],
                description=extract_description(detail_url) or "",
                mileage=extended_info['mileage'] or "",
                origin=extended_info['origin'] or "",
                body_type=extended_info['body_type'] or "",
                transmission=extended_info['transmission'] or "",
                engine=extended_info['engine'] or "",
                exterior_color=extended_info['exterior_color'] or "",
                interior_color=extended_info['interior_color'] or "",
                capacity=extended_info['capacity'] or "",
                number_of_doors=extended_info['number_of_doors'] or "",
                drive_train=extended_info['drive_train'] or "",
                seller_name=seller_info['seller_name'] or "",
                address_seller=seller_info['address_seller'] or "",
                phones=seller_info['phones'] or "",
            )
            
            print(f"cars_create: {cars_create}")
            cars_existed = cars_crud.get_car_by_car_id(db=db, car_id=cars_create.car_id)
            if cars_existed:
                print("------ EXISTED -------")
                continue
            
            cars_crud.create_car(db=db, car=cars_create)




def extract_general_info(content):
    anchor = content.find('a')
    cb1 = anchor.find('div', class_='cb1')
    
    return {
        "car_id": anchor.find('div', class_='cb5').find('span', class_='car_code').get_text().strip().split(':')[1].strip(),
        "name": anchor.find('div', class_='cb2_02').find('h3').get_text().strip().split('-')[0].strip(),
        "price": anchor.find('div', class_='cb3').find('b').get_text().strip(),
        "location": anchor.find('div', class_='cb4').find('b').get_text().strip(),
        "status": cb1.find(string=True, recursive=False).strip(),
        "year": cb1.find('b').get_text().strip(),
    }

def extract_extended_info(detail_url):
    resp = requests.get(detail_url, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Mapping labels to result keys
    label_mapping = {
        'Số Km đã đi:': 'mileage',
        'Xuất xứ:': 'origin',
        'Kiểu dáng:': 'body_type',
        'Hộp số:': 'transmission',
        'Động cơ:': 'engine',
        'Màu ngoại thất:': 'exterior_color',
        'Màu nội thất:': 'interior_color',
        'Số chỗ ngồi:': 'capacity',
        'Số cửa:': 'number_of_doors',
        'Dẫn động:': 'drive_train'
    }
    
    result = {key: None for key in label_mapping.values()}
    
    box_car = soup.find('div', id='sgg').find('div', class_='box_car_detail')
    
    for box_col in box_car.find_all('div', class_='col'):
        for col in box_col.find_all('div', id='mail_parent'):
            label = col.find('div', class_='label').find('label').get_text().strip()
            
            # Extract value from either txt_input or inputbox
            value_div = col.find('div', class_='txt_input') or col.find('div', class_='inputbox')
            if value_div:
                value = value_div.find('span', class_='inp').get_text().strip()
                
                # Map label to result key
                if label in label_mapping:
                    result[label_mapping[label]] = value
    
    return result

def extract_seller_info(detail_url):
    resp = requests.get(detail_url, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    contact_txt = soup.find('div', class_='contact-txt')

    # Extract seller name from span or a tag
    seller_name_tag = contact_txt.find('span', class_='cname') or contact_txt.find('a', class_='cname')
    seller_name = seller_name_tag.get_text().strip() if seller_name_tag else None

    # Extract address
    address_seller = next(
        (text.replace("Địa chỉ:", "").strip() for text in contact_txt.stripped_strings if text.startswith("Địa chỉ:")),
        None
    )
    
    # Extract phone numbers
    phones_list = [a.get_text(strip=True) for a in contact_txt.select('a[href^="tel:"]')]
    phones = ", ".join(phones_list) if phones_list else ""
    
    return {
        "seller_name": seller_name,
        "address_seller": address_seller,
        "phones": phones
    }

def extract_description(detail_url):
    resp = requests.get(detail_url, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    box_car_des = soup.find('div', class_='box_car_des')
    des_txt = box_car_des.find('div', class_= 'des_txt')
    description = des_txt.get_text().strip()
    return description

def extract_brand(detail_url):
    resp = requests.get(detail_url, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    breadcrum = soup.find('div', class_='breadcrum')
    brand = breadcrum.find_all('span', itemprop="name")[2].get_text().strip()
    return brand

def calc_total_page(url):
    # calc total page
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    cpage = soup.find('div', class_ = 'cpage').get_text().strip()
    match = re.search(r'/\s*([\d,.]+)', cpage)
    if match:
        pages = match.group(1).replace(',', '')
        return pages

    
if __name__ == "__main__":
    start_crawl()



