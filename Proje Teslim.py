#PROGRAM 221. SATIRDAN BAŞLIYOR
def tablo_olustur():
    baglanti = sqlite3.connect('kullanici_veritabani.db')
    imlec = baglanti.cursor()
    # Tablonun var olup olmadığını kontrol ediyoruz
    imlec.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kullanici'")
    table_exists = imlec.fetchone()

    if not table_exists:
        imlec.execute('''CREATE TABLE kullanici (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        kullanici_adi TEXT NOT NULL,
                        eposta TEXT NOT NULL,
                        sifre TEXT NOT NULL,
                        telefon TEXT NOT NULL,
                        yetki TEXT NOT NULL
                    )''')
        # Admini önceden tabloya ekliyoruz
        imlec.execute("INSERT INTO kullanici (kullanici_adi, eposta, sifre, telefon, yetki) VALUES (?, ?, ?, ?, ?)",
                      ("admin", "admin@posta.com", "admin123", "12345678901", "admin"))
        baglanti.commit()       
    baglanti.close()

def kullanici_kayit(kullanici_adi, eposta, sifre, telefon, yetki):
    baglanti = sqlite3.connect('kullanici_veritabani.db')
    imlec = baglanti.cursor()
    # Epostanın önceden kıyıtlı olup olmadığına bakıyoruz
    imlec.execute("SELECT COUNT(*) FROM kullanici WHERE eposta = ?", (eposta,))
    eposta_kayit_sayisi = imlec.fetchone()[0]
    if eposta_kayit_sayisi > 0:
        print("Bu e-posta zaten kayıtlı.")
        baglanti.close()
        return
    # Telefon numarasının önceden kıyıtlı olup olmadığına bakıyoruz
    imlec.execute("SELECT COUNT(*) FROM kullanici WHERE telefon = ?", (telefon,))
    telefon_kayit_sayisi = imlec.fetchone()[0]
    if telefon_kayit_sayisi > 0:
        print("Bu telefon numarası zaten kayıtlı.")
        baglanti.close()
        return
    imlec.execute("INSERT INTO kullanici (kullanici_adi, eposta, sifre, telefon, yetki) VALUES (?, ?, ?, ?, ?)",
                  (kullanici_adi, eposta, sifre, telefon, yetki))
    baglanti.commit()
    baglanti.close()
    print("Kayıt başarıyla oluşturuldu")

def ihtiyac_gonder(kategori, stok, kullanici_adi, eposta, telefon):
    while True:
        liste2 = []
        veriler = input("Lütfen ihtiyaçlarınızı virgülle ayırarak girin: ")
        print() #satır boşluğu için kullanıldı
        veri_listesi = veriler.lower().split(',')
        for veri in veri_listesi:
            if veri.strip() in stok:
                liste2.append(veri.strip())
                print("{} stokumuzda mevcut ihtiyaç listenize eklenmiştir.".format(veri.strip()))
            else:
                liste2.append(veri.strip())
                print("{} stokumuzda mevcut değil en kısa zamanda ihtiyaç listenize eklenecektir.".format(veri.strip()))
        print("İhtiyaç listeniz:", liste2)
        while True:
            onay = input("İhtiyaç listenizi onaylıyor musunuz? (evet/hayır): ")
            if onay.lower() == "evet":
                while True:
                    dongu = True
                    while dongu:
                        adres_verileri = input("İhtiyaçları göndermek istediğiniz adresi virgülle ayırarak giriniz (mahalle, sokak, numara, ilçe, il): ").lower()
                        try:
                            mahalle, sokak, numara, ilçe, il = adres_verileri.split(",")
                            adres = {
                                "Mahalle": mahalle.strip(),
                                "Sokak": sokak.strip(),
                                "Numara": numara.strip(),
                                "İlçe": ilçe.strip(),
                                "İl": il.strip()}
                            dongu = False 
                        except ValueError:
                            print("Adres bilgilerini eksik girdiniz lütfen bilgileri tekrar giriniz")
                    for key, value in adres.items():
                        print("{}: {}".format(key, value))
                    while True:
                        adres_onay = input("Adres bilgilerinizi onaylıyor musunuz? (evet/hayır): ")
                        if adres_onay.lower() == "evet":
                            #Bilgilerimizi excele yazdırma
                            import openpyxl
                            try:
                                workbook = openpyxl.load_workbook("kullanici_bilgileri.xlsx")
                                sheet = workbook.active
                            except FileNotFoundError:
                                workbook = openpyxl.Workbook()
                                sheet = workbook.active
                                sheet.append(["Kullanıcı Adı", "E-posta", "Telefon Numarası", "Kategori",
                                              "İhtiyaç Listesi", "Mahalle", "Sokak", "Numara", "İlçe", "İl" ])                          
                            yeni_satir = [kullanici_adi, eposta, telefon, kategori, ", ".join(liste2), mahalle, sokak, numara, ilçe, il]
                            sheet.append(yeni_satir)
                            workbook.save("kullanici_bilgileri.xlsx")
                            workbook.close()                           
                            break
                        elif adres_onay.lower() == "hayır":
                            break
                        else:
                            print("Lütfen sadece evet veya hayır cevaplarından birini verin.")
                    if adres_onay.lower() == "evet":
                        break
                bilgiler = {"Kullanıcı Adı": kullanici_adi,
                            "Telefon numarası": telefon,
                            "Adres": adres,
                            "Kategori": kategori,
                            "İhtiyaçları": liste2}
                for key, value in bilgiler.items():
                    print("{}: {}".format(key, value))
                print("İhtiyaçlarınızı en kısa zamanda gönderiyoruz. İyi günler dileriz.")
                import sys
                sys.exit()
            elif onay.lower() == "hayır":
                print("İşleminiz iptal ediliyor...")
                break
            else:
                print("Lütfen sadece evet veya hayır cevaplarından birini verin.")
                
def bagis_olustur():
    menü3="""
    Bağış Seçeneklerimiz 
    1)TL
    2)$(Dolar)   
    3)Crypto 
    4)Önceki menüye dön    
    """
    while True:
        print(menü3)
        bagis_secim = input("Lütfen bağış türünü seçiniz.(Önceki menüye dönmek için 4'e basınız.): ")
        if bagis_secim == "1":
            bagis_miktar = float(input("Bağışlamak istediğiniz mitarı giriniz: "))
            while True:
                bagis_onay = input("Bağışınız {} TL onaylıyor musunuz? (evet/hayır): ".format(bagis_miktar))
                if bagis_onay.lower() == "evet":
                    print("Yaptığınız {} TL bağış için teşekkür ederiz.".format(bagis_miktar))
                    break
                elif bagis_onay.lower() == "hayır":
                    print("İşleminiz iptal ediliyor...")
                    break
                else:
                    print("Lütfen sadece evet veya hayır cevaplarından birini verin.")
                    
        elif bagis_secim == "2":
            bagis_miktar2 = float(input("Bağışlamak istediğiniz mitarı giriniz: "))
            while True:
                bagis_onay2 = input("Bağışınız {} $ onaylıyor musunuz? (evet/hayır): ".format(bagis_miktar2))
                if bagis_onay2.lower() == "evet":
                    print("Yaptığınız {} $ bağış için teşekkür ederiz.".format(bagis_miktar2))
                    break
                elif bagis_onay2.lower() == "hayır":
                    print("İşleminiz iptal ediliyor...")
                    break
                else:
                    print("Lütfen sadece evet veya hayır cevaplarından birini verin.")
            
        elif bagis_secim == "3":
            crypto_menü="""
            1)Bitcoin (BTC)
            2)Ethereum (ETH)
            3)Binance Coin (BNB)
            4)Geri
            """
            while True:
                print(crypto_menü)
                crypto_secim = input("Bağışlamak istediğiniz crypto türünü seçiniz: ")
                if crypto_secim == "1":
                    crypto_bagis = float(input("Bağışlamak istediğiniz mitarı giriniz: "))
                    while True:
                        crypto_bagis_onay = input("Bağışınız {} BTC onaylıyor musunuz? (evet/hayır): ".format(crypto_bagis))
                        if crypto_bagis_onay.lower() == "evet":
                            print("Yaptığınız {} BTC bağış için teşekkür ederiz.".format(crypto_bagis))
                            break
                        elif crypto_bagis_onay.lower() == "hayır":
                            print("İşleminiz iptal ediliyor...")
                            break
                        else:
                            print("Lütfen sadece evet veya hayır cevaplarından birini verin.")
                    if crypto_bagis_onay.lower() == "evet": #165. satırdaki döngüden çıkmak için kullandık
                        break
                elif crypto_secim == "2":
                    crypto_bagis2 = float(input("Bağışlamak istediğiniz mitarı giriniz: "))
                    while True:
                        crypto_bagis_onay2 = input("Bağışınız {} ETH onaylıyor musunuz? (evet/hayır): ".format(crypto_bagis2))
                        if crypto_bagis_onay2.lower() == "evet":
                            print("Yaptığınız {} ETH bağış için teşekkür ederiz.".format(crypto_bagis2))
                            break
                        elif crypto_bagis_onay2.lower() == "hayır":
                            print("İşleminiz iptal ediliyor...")
                            break
                        else:
                            print("Lütfen sadece evet veya hayır cevaplarından birini verin.")
                    if crypto_bagis_onay2.lower() == "evet": #165. satırdaki döngüden çıkmak için kullandık
                        break
                elif crypto_secim == "3":
                    crypto_bagis3 = float(input("Bağışlamak istediğiniz mitarı giriniz: "))
                    while True:
                        crypto_bagis_onay3 = input("Bağışınız {} BNB onaylıyor musunuz? (evet/hayır): ".format(crypto_bagis3))
                        if crypto_bagis_onay3.lower() == "evet":
                            print("Yaptığınız {} BNB bağış için teşekkür ederiz.".format(crypto_bagis3))
                            break
                        elif crypto_bagis_onay3.lower() == "hayır":
                            print("İşleminiz iptal ediliyor...")
                            break
                        else:
                            print("Lütfen sadece evet veya hayır cevaplarından birini verin.")
                    if crypto_bagis_onay3.lower() == "evet": #165. satırdaki döngüden çıkmak için kullandık
                        break
                elif crypto_secim == "4":
                    print("İşleminiz iptal ediliyor...")
                    break
                else:
                    print("Geçerli bir işlem giriniz.")
        elif bagis_secim == "4":
            print("Önceki menüye dönülüyor...")
            break
        else:
            print("Lütfen geçerli bir işlem giriniz.")

#PROGRAM BURADAN BAŞLIYOR
import sqlite3 
import pandas as pd       
menü1="""
1)Kayıt Ol
2)Giriş Yap
3)Şifremi Unuttum
4)Çıkış Yap
"""
yanlis_giris_sayaci = 3
while True: 
    print(menü1)
    tablo_olustur()
    try:
        secim = int(input("Yapmak istediğiniz işlemi seçiniz: ")) #Sadece birden dörde kadar olan sayılar girilir 
        while secim<1 or secim>4:                             
            secim = int(input("Lütfen 1 ile 4 arasında bir sayı giriniz:"))
            break
    except ValueError:
        print("Lütfen sayı giriniz!")
    if secim == 1:
        #Kullanıcı Adı
        while True:
            kullanici_adi = input("Kullanıcı adı belirleyiniz: ") #Kullanıcı adı en az beş karakter olmalıdır
            if len(kullanici_adi)<5:    
                print("Kullanıcı adı en az beş karakterden oluşmalıdır")
            else:
                print("Kullanıcı adınız geçerlidir")
                break
        #E-posta
        while True:
            eposta = input("E-posta adresinizi giriniz: ") #Eposta adresi olabilmesi için "@" ve "." içermelidir         
            if ("@" not in eposta) or ("." not in eposta):
                print("Üzgünüm bu geçerli bir e-posta adresi değildir")    
            else:
                break
        #Şifre
        while True:
            sifre = input("Bir şifre belirleyiniz: ")
            sifre_tekrar = input("Şifrenizi tekrar giriniz: ")
            if sifre == sifre_tekrar:
                print("Şifreniz geçerli şifreler eşleşti.")
                break
            else:
                print("Şifreler eşleşmiyor")
        #Telefon Numarası
        while True:
            telefon = input("Telefon numaranızı giriniz: ") #Numara 11 haneli ve sayı içermelidir
            if telefon.isdigit() and len(telefon)==11:
                break
            else:
                print("Telefon numarası 11 haneli ve rakamlardan oluşmalıdır")                 
        yetki = "normal" # Kayıt olan kullanıcılar normal yetkiye sahip olacak
        kullanici_kayit(kullanici_adi, eposta, sifre, telefon, yetki)
            
    elif secim == 2:
        eposta = input("Epostanızı giriniz: ")
        sifre = input("Şifrenizi giriniz: ")
        baglanti = sqlite3.connect('kullanici_veritabani.db')
        imlec = baglanti.cursor()
        imlec.execute("SELECT yetki FROM kullanici WHERE eposta = ? AND sifre = ?", (eposta, sifre))
        satir = imlec.fetchone()
        if satir is not None:
            yetki = satir[0]
            if yetki == 'admin':
                print("Admin olarak giriş yapıldı.")
                # Admin kullanıcılar için yapılması gereken işlemler              
                class Admin:
                    def __init__(self):
                        self.baglanti = sqlite3.connect('kullanici_veritabani.db')  
                        self.imlec = self.baglanti.cursor()
                    #kullanıcı kaydını silme işlemi
                    def kullanici_sil(self, eposta):
                        self.imlec.execute("DELETE FROM kullanici WHERE eposta=?", (eposta,))
                        if self.imlec.rowcount > 0:
                            self.baglanti.commit()
                            print("Kullanıcı başarıyla silindi.")
                        else:
                            print("Kullanıcı bulunamadı.")
                    #kullanıcının sipariş geçmişini göster işlemi
                    def tum_siparisleri_goster(self, eposta):
                        df = pd.read_excel("kullanici_bilgileri.xlsx")        
                        filtre_eposta = df["E-posta"] == eposta                            
                        ihtiyac_listesi = df.loc[filtre_eposta, "İhtiyaç Listesi"]
                        filtre_ihtiyac = df["İhtiyaç Listesi"].apply(lambda x: any(item in x for item in ihtiyac_listesi))
                        filtrelenmis_veriler = df[filtre_eposta & filtre_ihtiyac]
                        if not filtrelenmis_veriler.empty:
                            for index, kullanici_bilgileri in filtrelenmis_veriler.iterrows():
                                print("Kullanıcı Adı:", kullanici_bilgileri["Kullanıcı Adı"])
                                print("E-posta:", kullanici_bilgileri["E-posta"])
                                print("Telefon Numarası:", kullanici_bilgileri["Telefon Numarası"])
                                print("Kategori:", kullanici_bilgileri["Kategori"])
                                print("İhtiyaç Listesi:", kullanici_bilgileri["İhtiyaç Listesi"])
                                print("Mahalle:", kullanici_bilgileri["Mahalle"])
                                print("Sokak:", kullanici_bilgileri["Sokak"])
                                print("Numara:", kullanici_bilgileri["Numara"])
                                print("İlçe:", kullanici_bilgileri["İlçe"])
                                print("İl:", kullanici_bilgileri["İl"])
                                print()
                        else:
                            print("Belirtilen e-postaya sahip kullanıcı bulunamadı.")
                    #kullanıcının siparişlerini iptal etme işlemi
                    def siparis_iptal(self, eposta):
                        df = pd.read_excel("kullanici_bilgileri.xlsx")
                        filtre2 = df["E-posta"] == eposta
                        kayit = df[filtre2]                 
                        if kayit.empty:
                            print("Bu epostaya sahip kullanıcı bulunamadı.")
                        else:                        
                            df = df.drop(kayit.index)                          
                            df.to_excel('kullanici_bilgileri.xlsx', index=False)                       
                            print("Kullanıcının siparişleri iptal edildi.")
                                                                   
                    def admin_islemleri(self):
                        admin_menü="""
                    1)Kullanıcıyı sil
                    2)Kullanıcının sipariş geçmişini göster  
                    3)Kullanıcının siparişlerini iptal et 
                    4)Ana memüye dön                   
                    """
                        while True:
                            print(admin_menü)          
                            menü_secim= input("Lütfen işlem seçin: ")
                            if menü_secim == "1":
                                eposta = input("Silinecek kullanıcının e-posta adresini girin: ")
                                self.kullanici_sil(eposta)             

                            elif menü_secim == "2":
                                eposta = input("Siparişleri gösterilecek kullanıcının e-posta adresini girin: ")                      
                                self.tum_siparisleri_goster(eposta)
            
                            elif menü_secim =="3":
                                eposta = input("Siparişini iptal etmek istediğniz kullanıcının epostasını girin: ")
                                self.siparis_iptal(eposta)
            
                            elif menü_secim == "4":
                                break
                            else:
                                print("Lütfen geçerli bir seçenek giriniz.")
                admin = Admin()
                admin.admin_islemleri()
           
            elif yetki == 'normal':
                # Normal kullanıcılar için yapılması gereken işlemler
                print("Başarıyla giriş yapıldı.")
                menü2="""
                1)Yangın ihtiyaç listesi                             
                2)Deprem ihtiyaç listesi  
                3)Sel ihtiyaç listesi  
                4)Heyelan(Toprak Kayması) ihtiyaç listesi  
                5)Bağış İşlemleri
                6)Ana menüye dön
                """
                while(True):
                    print(menü2)
                    seçim=input("Lütfen yapmak istediğiniz işlemi seçiniz: ")   
                    if seçim=="1":
                        kategori = "Yangın"
                        stok = ("yangın söndürme tüpü", "yanmaz eldiven", "gıda", "su", "ilk yardım malzemesi", "çadır", "battaniye")
                        imlec.execute("SELECT kullanici_adi, telefon FROM kullanici WHERE eposta=?", (eposta,))
                        result = imlec.fetchone()
                        kullanici_adi = result[0]
                        telefon = result[1]
                        ihtiyac_gonder(kategori, stok, kullanici_adi, eposta, telefon)
                        
                    elif seçim=="2":
                        kategori="Deprem"
                        stok = ("iletişim araçları", "el feneri", "jeneratör", "çadır", "battaniye", "gıda", "su", "ilk yardım malzemesi")
                        imlec.execute("SELECT kullanici_adi, telefon FROM kullanici WHERE eposta=?", (eposta,))
                        result = imlec.fetchone()
                        kullanici_adi = result[0]
                        telefon = result[1]
                        ihtiyac_gonder(kategori, stok, kullanici_adi, eposta, telefon)
                           
                    elif seçim=="3":
                        kategori = "Sel"
                        stok = ("halat", "çizme", "kurtarma botu", "çadır", "ilk yardım malzemesi", "gıda", "su" ,"battaniye")
                        imlec.execute("SELECT kullanici_adi, telefon FROM kullanici WHERE eposta=?", (eposta,))
                        result = imlec.fetchone()
                        kullanici_adi = result[0]
                        telefon = result[1]
                        ihtiyac_gonder(kategori, stok, kullanici_adi, eposta, telefon)        
                 
                    elif seçim=="4":
                        kategori="Heyelan"
                        stok = ("kazma", "kürek", "çadır", "ilk yardım malzemesi", "gıda", "su" ,"battaniye")
                        imlec.execute("SELECT kullanici_adi, telefon FROM kullanici WHERE eposta=?", (eposta,))
                        result = imlec.fetchone()
                        kullanici_adi = result[0]
                        telefon = result[1]
                        ihtiyac_gonder(kategori, stok, kullanici_adi, eposta, telefon)                 

                    elif seçim=="5":
                        bagis_olustur() 
                        
                    elif seçim=="6":
                        print("Ana menüye dönülüyor...")
                        break
                    else:
                        print("Lütfen geçerli bir işlem giriniz.")   
        else:
            yanlis_giris_sayaci-=1
            print("Eposta veya şifreniz yanlış. Kalan giriş hakkınız:", yanlis_giris_sayaci)
        if yanlis_giris_sayaci == 0:
            print("Yanlış giriş hakkınızı doldurdunuz. Program sonlanıyor...")
            import sys
            sys.exit()               
        baglanti.close()
        
    elif secim == 3:
        while True:
            eposta_kontrol = input("E-posta adresinizi giriniz: ")     
            if ("@" not in eposta_kontrol) or ("." not in eposta_kontrol):
                print("Üzgünüm, bu geçerli bir e-posta adresi değildir")    
            else:
                break
        baglanti = sqlite3.connect('kullanici_veritabani.db')
        imlec = baglanti.cursor()
        imlec.execute("SELECT eposta, sifre FROM kullanici WHERE eposta=?", (eposta_kontrol,))
        result = imlec.fetchone()
        if result is not None:
            eposta = result[0]
            sifre = result[1]
            import random
            rastgele_sayi = random.randint(100, 999)
            with open("sayi.txt", "w") as dosya:
                dosya.write(str(rastgele_sayi))
            sayi_kontrol = input("E-posta adresinize bir doğrulama kodu gönderdik, lütfen kodu giriniz: ")
            if sayi_kontrol == str(rastgele_sayi):
                while True:
                    yeni_sifre = input("Yeni şifrenizi giriniz: ")
                    yeni_sifre_tekrar = input("Yeni şifrenizi tekrar giriniz: ")
                    if yeni_sifre == yeni_sifre_tekrar:
                        if yeni_sifre == sifre:
                            print("Yeni şifreniz eski şifrenizle aynı olamaz")
                        else:    
                            imlec.execute("UPDATE kullanici SET sifre = ? WHERE eposta = ?", (yeni_sifre , eposta))
                            baglanti.commit()
                            print("Şifreniz güncellendi.")
                            break
                    else:
                        print("Şifreler eşleşmiyor")                               
            else:
                print("Girdiğiniz kod yanlış")
        else:
            print("E-posta sisteme kayıtlı değil")       
    
    elif secim == 4:
        print("Çıkış yapılıyor...")
        break  
    else:
        print("Geçersiz seçenek.")
