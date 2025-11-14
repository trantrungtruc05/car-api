from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import time
from app.core.database import get_db
from app.crud import category_crud
from app.schemas import CategoryCreate

BASE_URL = "https://bonbanh.com/"

def make_driver(headless=True):
    opts = webdriver.ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")
    

    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--window-size=1366,900")
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) " 
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/127.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    return driver

def click_show_all_if_exists(driver):
    try:
        
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "o_make_lnk"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        time.sleep(0.2)
        btn.click()
        
        time.sleep(0.3)
    except Exception:
        pass

def extract_brands(driver):
    brands = []
    seen = set()

    
    nav = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#primary-nav"))
    )

    li_nodes = nav.find_elements(By.CSS_SELECTOR, "li.menuparent")

    for li in li_nodes:
        title_nodes = li.find_elements(By.CSS_SELECTOR, ".mtop-item")

        print(len(title_nodes))
        
        if not title_nodes:
            continue

        title = title_nodes[0]
        name = title.text.strip()
        if not name:
            continue

        # Lấy link: a@href hoặc span@url
        href = ""
        tag_name = title.tag_name.lower()
        if tag_name == "a":
            href = (title.get_attribute("href") or "").strip()
        else:
            href = (title.get_attribute("url") or "").strip()
            if href:
                href = urljoin(BASE_URL, href)

        if not href:
            # Không có link thì bỏ qua để tránh rác
            continue

        if name not in seen:
            seen.add(name)
            brands.append({"brand": name, "href": href})

    return brands

def start_crawl():
    driver = make_driver(headless=True)
    try:
        driver.get(BASE_URL)

        # Nếu site lazy load/đổi layout, cho thở 1 nhịp
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#primary-nav"))
        )

        click_show_all_if_exists(driver)

        brands = extract_brands(driver)

        for b in brands:
            print(f"- {b['brand']}: {b['href']}")

        # save into database
        db = next(get_db())
        for b in brands:
            categoryCreate = CategoryCreate(
                name=b['brand'],
                link=b['href'],
                code=b['brand']
            )
            category = category_crud.get_category_by_code(db=db, code=b['brand'])
            if category:
                continue
            else:
                category = category_crud.create_category(db=db, category=categoryCreate)
                print(f"Created category: {category.name}")

    finally:
        driver.quit()