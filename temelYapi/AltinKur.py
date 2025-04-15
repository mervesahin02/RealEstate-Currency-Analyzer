from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, traceback

# ─────────────────────────────────────────────────────────────────────────────
def get_max_day(year, month):
    ay, yil = int(month), int(year)
    if ay in (1, 3, 5, 7, 8, 10, 12):
        return 31
    if ay in (4, 6, 9, 11):
        return 30
    return 29 if (yil % 4 == 0 and yil % 100 != 0) or (yil % 400 == 0) else 28

# ─────────────────────────────────────────────────────────────────────────────
def safe_click(elem, driver, wait):
    try:
        wait.until(EC.element_to_be_clickable(elem)).click()
    except Exception:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        driver.execute_script("arguments[0].click();", elem)

def select_day_with_diff_message(driver, wait, day_num: int) -> int:
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.ui-datepicker-calendar")))
    calendar = driver.find_element(By.CSS_SELECTOR, "table.ui-datepicker-calendar")

    rows = calendar.find_elements(By.CSS_SELECTOR, "tbody tr")
    gun_str = str(day_num)

    for row_index, row in enumerate(rows):
        cells = row.find_elements(By.TAG_NAME, "td")
        for i, td in enumerate(cells):
            text = td.get_attribute("innerText").strip()
            if text == gun_str:
                # ✅ Gün bulundu
                a = td.find_elements(By.CSS_SELECTOR, "a.ui-state-default")
                if a:
                    safe_click(a[0], driver, wait)
                    print(f"✅ {day_num}. gün seçildi (aktifti).")
                    return day_num
                else:
                    # ⬅ Solundaki günlere bakarak ilk aktif günü bul
                    for j in range(i - 1, -1, -1):
                        left_td = cells[j]
                        left_a = left_td.find_elements(By.CSS_SELECTOR, "a.ui-state-default")
                        if left_a:
                            selected_day = int(left_a[0].text.strip())
                            diff = day_num - selected_day
                            safe_click(left_a[0], driver, wait)
                            print(f"⬅ {day_num}. gün pasifti, {selected_day}. gün seçildi ({diff} gün önce).")
                            return selected_day
                    raise Exception(f"❌ {day_num}. gün pasifti ve satırda daha önce seçilebilir gün yok.")
    raise Exception(f"❌ {day_num}. gün DOM’da bulunamadı.")


# ─────────────────────────────────────────────────────────────────────────────
yil = input("Yıl girin (örn: 2025): ").strip()
ay_girdi = input("Ay girin (örn: 01 Ocak): ").strip()
gun_inp = input("Gün girin (örn: 14): ").strip()
gun = int(gun_inp)

try:
    ay_numarasi, _ = ay_girdi.split(" ")
    data_month = str(int(ay_numarasi) - 1)          # 01 → 0
    gun = int(gun_inp)
except ValueError:
    print("❗ Lütfen doğru formatta tarih girin.")
    exit()

max_gun = get_max_day(int(yil), int(ay_numarasi))
if not (1 <= gun <= max_gun):
    print(f"❗ Bu ay {max_gun} gün çekiyor. 1‑{max_gun} arası girin.")
    exit()

# ─────────────────────────────────────────────────────────────────────────────
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Temp\\ChromeProfile_TCMB")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

try:
    driver.get("https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb+tr/main+menu/istatistikler/doviz+kurlari/saat+basi+belirlenen+doviz+kurlari+ve+altin+fiyatlari")
    print("Sayfa yüklendi.")

    # YIL SEÇİMİ
    while True:
        yil_dugmeleri = driver.find_elements(
            By.XPATH,
            "//a[contains(@class,'block-tabs-tab') and contains(@class,'w-tab-link') and @data-year]"
        )
        bulundu = False
        for dugme in yil_dugmeleri:
            if dugme.get_attribute("data-year") == yil:
                if "w--current" not in dugme.get_attribute("class"):
                    dugme.click()
                print(f"✅ Yıl seçildi: {yil}")
                bulundu = True
                break
        if bulundu:
            break
        ileri = driver.find_elements(By.XPATH, "//a[contains(@class,'next')]")
        if not ileri:
            raise Exception(f"{yil} yılı bulunamadı.")
        ileri[0].click()
        time.sleep(0.8)

    # AY SEÇİMİ
    ay_xpath = (
        f"//div[contains(@class,'calendar-months')]"
        f"//a[contains(@class,'calendar-month') and @data-month='{data_month}' and @data-year='{yil}']"
    )
    wait.until(EC.element_to_be_clickable((By.XPATH, ay_xpath))).click()
    print(f"✅ Ay seçildi: {ay_girdi}")

    # GÜN SEÇİMİ
    # 📅 GÜN SEÇİMİ
    wait.until(EC.presence_of_element_located((By.XPATH, "//table[@class='ui-datepicker-calendar']/tbody/tr[1]/td")))
    gun = select_day_with_diff_message(driver, wait, gun)



    # GÖSTER
    goster_xpath = "//input[@type='submit' and @value='Göster']"
    goster = wait.until(EC.presence_of_element_located((By.XPATH, goster_xpath)))
    if goster.get_attribute("disabled"):
        raise Exception("Seçilen tarih için veri yok, Göster butonu pasif.")
    safe_click(goster, driver, wait)
    print("📥 Göster butonuna tıklandı.")

    # KUR TABLOSU
    tablo_xpath = "//table[@class='kurlarTablo']"
    wait.until(EC.presence_of_element_located((By.XPATH, tablo_xpath)))
    print("📊 Kur tablosu yüklendi.")

    altin_xpath = "//td[contains(text(),'Altın/TRY')]/following-sibling::td[@class='deger']"
    altin_deger = driver.find_element(By.XPATH, altin_xpath).text
    print(f"Altın/TRY: {altin_deger}")

except (TimeoutException, NoSuchElementException, Exception):
    print("\n❗ Bir hata oluştu:")
    traceback.print_exc()
finally:
    driver.quit()