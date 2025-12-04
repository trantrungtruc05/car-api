from math import e
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from app.core.database import get_db
from app.schemas.car_schema import CarsCreate
from app.crud import cars_crud
import re
from app.utils.number_utils import convert_price_to_number, convert_mileage_to_integer
import random
import time
from app.crud.cron_info_repo import cron_info_crud
from datetime import datetime
from datetime import timezone

BASE_URL = "https://bonbanh.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
}

delay = random.uniform(2, 5) 

def start_crawl(start_page, end_page):

    db = next(get_db())

    # update run_at of cron info
    cron_info_crud.update_cron_info_run_at(db=db, job_name="car_crawler", run_at=datetime.now(timezone.utc))

    for page in range(start_page, end_page):
        resp = requests.get(BASE_URL + f"oto/page,{page}", headers=headers, timeout=10)
        print(BASE_URL + f"oto/page,{page} with delay: {delay}s")
        resp.raise_for_status()

        html = resp.text
        soup = BeautifulSoup(html, "html.parser")

        h_list_car = soup.find('div', id='s-list-car')
        g_box_content = h_list_car.find('div', class_='g-box-content')

        for content in g_box_content.find_all('li', class_='car-item'):
            name = content.find('a')['href']
            print(urljoin(BASE_URL, name))
            
            
            general_info = extract_general_info(content)
            
            cars_existed = cars_crud.get_car_by_car_id(db=db, car_id=general_info['car_id'])
            if cars_existed:
                print("------ EXISTED -------")
                continue
            else:
                # Extract data once to avoid multiple requests
                detail_url = urljoin(BASE_URL, name)
                extended_info = extract_extended_info(detail_url)

                # insert into cars table
                cars_create = CarsCreate(
                car_id=general_info['car_id'],
                brand = extended_info['brand'] or "",
                name=general_info['name'],
                price= convert_price_to_number(general_info['price']),
                location=general_info['location'],
                status=general_info['status'],
                year=general_info['year'],
                description=extended_info['description'] or "",
                mileage=convert_mileage_to_integer(extended_info['mileage']),
                origin=extended_info['origin'] or "",
                body_type=extended_info['body_type'] or "",
                transmission=extended_info['transmission'] or "",
                engine=extended_info['engine'] or "",
                exterior_color=extended_info['exterior_color'] or "",
                interior_color=extended_info['interior_color'] or "",
                capacity=extended_info['capacity'] or "",
                number_of_doors=extended_info['number_of_doors'] or "",
                drive_train=extended_info['drive_train'] or "",
                seller_name=extended_info['seller_name'] or "",
                address_seller=extended_info['address_seller'] or "",
                phones=extended_info['phones'] or "",
                link=detail_url,
            )
            
                print(f"cars_create: {cars_create}")
                cars_crud.create_car(db=db, car=cars_create)

    # update run_end_at of cron info
    cron_info_crud.update_cron_info_run_end_at(db=db, job_name="car_crawler", run_end_at=datetime.now(timezone.utc))




def extract_general_info(content):
    anchor = content.find('a')
    cb1 = anchor.find('div', class_='cb1')
    year = cb1.find('b').get_text().strip()
    if'<' in year:
        return None
    
    return {
        "car_id": anchor.find('div', class_='cb5').find('span', class_='car_code').get_text().strip().split(':')[1].strip(),
        "name": anchor.find('div', class_='cb2_02').find('h3').get_text().strip().split('-')[0].strip(),
        "price": convert_price_to_number(anchor.find('div', class_='cb3').find('b').get_text().strip()),
        "location": anchor.find('div', class_='cb4').find('b').get_text().strip(),
        "status": cb1.find(string=True, recursive=False).strip(),
        "year": year
        
    }

def extract_extended_info(detail_url):
    time.sleep(1)
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

    # seller info
    contact_txt = soup.find('div', class_='contact-txt')

    seller_name_tag = contact_txt.find('span', class_='cname') or contact_txt.find('a', class_='cname')
    seller_name = seller_name_tag.get_text().strip() if seller_name_tag else None

    address_seller = next(
        (text.replace("Địa chỉ:", "").strip() for text in contact_txt.stripped_strings if text.startswith("Địa chỉ:")),
        None
    )
    
    phones_list = [a.get_text(strip=True) for a in contact_txt.select('a[href^="tel:"]')]
    phones = ", ".join(phones_list) if phones_list else ""

    result.seller_name = seller_name
    result.address_seller = address_seller
    result.phones = phones

    # description
    box_car_des = soup.find('div', class_='box_car_des')
    des_txt = box_car_des.find('div', class_= 'des_txt')
    description = des_txt.get_text().strip()
    result.description = description

    # brand
    breadcrum = soup.find('div', class_='breadcrum')
    brand = breadcrum.find_all('span', itemprop="name")[2].get_text().strip()
    result.brand = brand

    return result


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



