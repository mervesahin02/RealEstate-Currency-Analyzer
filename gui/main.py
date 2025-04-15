from tkinter import *
from tkinter import messagebox
import subprocess, os

from widgets import create_labeled_entry
import styles

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANALIZ_PATH = os.path.join(BASE_DIR, "..", "ArsaTakipSistemi", "arsa_analiz.py")

def hesapla():
    try:
        values = [e.get() for e in all_entries]
        input_data = "\n".join(values) + "\n"
        result = subprocess.run(
            ["python", ANALIZ_PATH],
            input=input_data,
            capture_output=True,
            text=True,
            encoding="utf-8"  # ✅ BU ÇOK ÖNEMLİ!
        )
        output_text.delete("1.0", END)
        output_text.insert("1.0", result.stdout)  # ✅ DOĞRU KULLANIM
    except Exception as e:
        messagebox.showerror("Hata", str(e))


root = Tk()
root.title(styles.APP_TITLE)
root.geometry("1000x600")
root.configure(bg=styles.BG_COLOR)

Label(root, text="📌 Alım Bilgileri", font=styles.TITLE_FONT, bg=styles.BG_COLOR).grid(row=0, column=0, columnspan=5, pady=5)
alim_yil     = create_labeled_entry(root, "Yıl girin (örn: 2020):",        1, 0)
alim_ay      = create_labeled_entry(root, "Ay girin (örn: 12 Aralık):",         1, 1)
alim_gun     = create_labeled_entry(root, "Gün girin (örn: 14): ",        1, 2)
alim_m2      = create_labeled_entry(root, "Alınan metrekare:",  1, 3)
alim_tl      = create_labeled_entry(root, "Toplam alım fiyatı (₺):",  1, 4)

Label(root, text="📌 Satış Bilgileri", font=styles.TITLE_FONT, bg=styles.BG_COLOR).grid(row=3, column=0, columnspan=5, pady=5)
satis_yil    = create_labeled_entry(root, "Yıl girin (örn: 2021):",        4, 0)
satis_ay     = create_labeled_entry(root, "Ay girin (örn: 01 Ocak):",         4, 1)
satis_gun    = create_labeled_entry(root, "Gün girin (örn: 2): ",        4, 2)
satis_m2     = create_labeled_entry(root, "Satılan metrekare:",  4, 3)
satis_tl     = create_labeled_entry(root, "Toplam satış fiyatı (₺):",  4, 4)

all_entries = [alim_yil, alim_ay, alim_gun, alim_m2, alim_tl,
               satis_yil, satis_ay, satis_gun, satis_m2, satis_tl]

Button(root, text="📥 Hesapla", bg=styles.BTN_COLOR, fg=styles.BTN_TEXT_COLOR,
       font=("Helvetica", 10, "bold"), command=hesapla).grid(row=6, column=0, columnspan=5, pady=10)

output_text = Text(root, width=120, height=22, font=styles.TEXT_FONT)
output_text.grid(row=7, column=0, columnspan=5, padx=10)

root.mainloop()
