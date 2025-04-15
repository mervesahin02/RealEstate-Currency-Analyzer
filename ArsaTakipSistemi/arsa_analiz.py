from kurlar import get_kurlar

def hesapla_oran(eski, yeni):
    if eski == 0:
        return 0.0
    return round(((yeni - eski) / eski) * 100, 2)

def format_para(deger):
    return f"{deger:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")

def main():
    print("📌 Alım Bilgileri:")
    alim_yil = input("Yıl girin (örn: 2020): ").strip()
    alim_ay = input("Ay girin (örn: 12 Aralık): ").strip()
    alim_gun = input("Gün girin (örn: 14): ").strip()
    alim_m2 = float(input("Alınan metrekare: "))
    alim_tl = float(input("Toplam alım fiyatı (₺): "))

    print("\n📌 Satış Bilgileri:")
    satis_yil = input("Yıl girin (örn: 2025): ").strip()
    satis_ay = input("Ay girin (örn: 03 Mart): ").strip()
    satis_gun = input("Gün girin (örn: 10): ").strip()
    satis_m2 = float(input("Satılan metrekare: "))
    satis_tl = float(input("Toplam satış fiyatı (₺): "))

    print("\n🔁 Kurlar çekiliyor...")
    alim_kur = get_kurlar(alim_yil, alim_ay, alim_gun)
    satis_kur = get_kurlar(satis_yil, satis_ay, satis_gun)

    # Metrekare fiyatı
    alim_m2_fiyat = alim_tl / alim_m2
    satis_m2_fiyat = satis_tl / satis_m2

    # Kur karşılıkları
    alim_usd = alim_tl / alim_kur["usd"]
    alim_eur = alim_tl / alim_kur["eur"]
    alim_altin = alim_tl / alim_kur["altin"]

    satis_usd = satis_tl / satis_kur["usd"]
    satis_eur = satis_tl / satis_kur["eur"]
    satis_altin = satis_tl / satis_kur["altin"]

    print("\n==============================")
    print("▶ ALIM:")
    print(f"Metrekare Fiyatı: ₺{format_para(alim_m2_fiyat)}")
    print(f"Dolar: {alim_kur['usd']} ₺ → ${format_para(alim_usd)}")
    print(f"Euro: {alim_kur['eur']} ₺ → €{format_para(alim_eur)}")
    print(f"Altın: {alim_kur['altin']} ₺ → {format_para(alim_altin)} gr")

    print("\n▶ SATIŞ:")
    print(f"Metrekare Fiyatı: ₺{format_para(satis_m2_fiyat)}")
    print(f"Dolar: {satis_kur['usd']} ₺ → ${format_para(satis_usd)}")
    print(f"Euro: {satis_kur['eur']} ₺ → €{format_para(satis_eur)}")
    print(f"Altın: {satis_kur['altin']} ₺ → {format_para(satis_altin)} gr")

    print("\n📈 DEĞİŞİM ORANLARI:")
    print(f"Metrekare Fiyatı: %{hesapla_oran(alim_m2_fiyat, satis_m2_fiyat)}")
    print(f"Toplam TL: %{hesapla_oran(alim_tl, satis_tl)}")
    print(f"Dolar: %{hesapla_oran(alim_usd, satis_usd)}")
    print(f"Euro: %{hesapla_oran(alim_eur, satis_eur)}")
    print(f"Altın: %{hesapla_oran(alim_altin, satis_altin)}")

if __name__ == "__main__":
    main()
