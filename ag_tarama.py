import scapy.all as scapy
from tkinter import *
from tkinter import messagebox
import subprocess

def ip_adress():
    try:
        # IP adresini almak için subprocess komutunu çalıştır
        ip_deger = subprocess.run(["ipconfig", "getifaddr", "en0"], capture_output=True, text=True, check=True)
        ip_address = ip_deger.stdout.strip()  # IP adresini al ve ekstra boşlukları temizle
        label3.config(text=ip_address)  # Label'i IP adresi ile güncelle
    except subprocess.CalledProcessError:
        messagebox.showerror("Hata", "IP adresi alınamadı. Lütfen bağlantınızı kontrol edin.")

def tarama():
    # Listbox'ı temizle
    liste.delete(0, END)

    ip = entry1.get()  # Kullanıcının girdiği IP aralığını al
    if not ip:
        messagebox.showwarning("Uyarı", "Lütfen bir IP aralığı girin.")
        return

    arp_istek = scapy.ARP(pdst=ip)
    broadcast_istek = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    birlesmis_paket = broadcast_istek / arp_istek
    try:
        (tanimli_liste, tanimsiz_liste) = scapy.srp(birlesmis_paket, timeout=1, verbose=False)
        for paket in tanimli_liste:
            # Her paketin kaynak IP adresi, kaynak MAC adresi ve hedef IP adresi bilgilerini al
            kaynak_ip = paket[1].psrc
            kaynak_mac = paket[1].hwsrc
            hedef_ip = paket[1].pdst
            hedef_mac = paket[1].hwdst
            bilgi = f"Kaynak IP: {kaynak_ip}, Kaynak MAC: {kaynak_mac}, Hedef IP: {hedef_ip}, Hedef MAC: {hedef_mac}"
            liste.insert(END, bilgi)
    except PermissionError:
        messagebox.showerror("Hata", "İzin hatası: Lütfen scripti root olarak çalıştırın.")
    except Exception as e:
        messagebox.showerror("Hata", f"Beklenmeyen bir hata oluştu: {e}")

# Ana pencereyi oluşturma
pencere1 = Tk()
pencere1.title("Ağ Tarama Aracı")
pencere1.geometry("900x400")

# Kullanıcıdan IP aralığı alma
label1 = Label(pencere1, text="Lütfen tarama yapmak istediğiniz IP aralığını giriniz:")
label1.pack()
entry1 = Entry(pencere1)
entry1.pack()

# Tarama butonu
buton1 = Button(pencere1, text="Tarama yapmak için tıklayın", command=tarama)
buton1.pack()

# Listbox oluşturma
liste = Listbox(pencere1, width=100)
liste.pack(pady=20)

# IP adresini öğrenme butonu
label2 = Label(pencere1, text="IP adresinizi öğrenmek için tıklayın:")
label2.pack()
label3 = Label(pencere1, text="IP adresi burada görünecek")  # IP adresi için yer tutucu
label3.pack()
buton2 = Button(pencere1, text="IP adresini öğren", command=ip_adress)
buton2.pack()

# Ana döngüyü başlatma
pencere1.mainloop()
