import subprocess
import re
import os

# Bu dosyanın bulunduğu dizini al (ArsaTakipSistemi klasörü)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_altin_kuru(yil, ay, gun):
    altin_path = os.path.join(BASE_DIR, "Altin.py")
    result = subprocess.run(
        ["python", altin_path],
        input=f"{yil}\n{ay}\n{gun}\n",
        text=True,
        capture_output=True,
        encoding="utf-8"  # 🔥 işte burası!
    )
    output = result.stdout

    match = re.search(r"Altın/TRY: ([\d,.]+)", output)
    if not match:
        print("🔍 Altın çıktısı:")
        print(output)
        print("❌ stderr:", result.stderr)
        raise Exception("❌ Altın kuru bulunamadı.")

    return float(match.group(1).replace(",", ".").replace(".", "", match.group(1).count(".") - 1))


def get_dolar_euro(yil, ay, gun):
    de_path = os.path.join(BASE_DIR, "DolarEuro.py")
    result = subprocess.run(
        ["python", de_path],
        input=f"{yil}\n{ay}\n{gun}\n",
        text=True,
        capture_output=True,
        encoding="utf-8"  # 🔥 burası da şart
    )

    output = result.stdout

    usd_match = re.search(r"USD: ([\d,.]+)", output)
    eur_match = re.search(r"EUR: ([\d,.]+)", output)
    if not usd_match or not eur_match:
        print("🔍 Dolar-Euro çıktısı:")
        print(output)
        print("❌ stderr:", result.stderr)
        raise Exception("❌ Dolar/Euro kuru bulunamadı.")

    usd = float(usd_match.group(1).replace(",", ".").replace(".", "", usd_match.group(1).count(".") - 1))
    eur = float(eur_match.group(1).replace(",", ".").replace(".", "", eur_match.group(1).count(".") - 1))
    return usd, eur


def get_kurlar(yil, ay, gun):
    altin = get_altin_kuru(yil, ay, gun)
    usd, eur = get_dolar_euro(yil, ay, gun)
    return {"altin": altin, "usd": usd, "eur": eur}
