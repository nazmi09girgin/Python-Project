menü="""
1)Kayıt Ol
2)Giriş Yap
3)Şifremi Unuttum
4)Çıkış Yap
"""
print(menü)
while(True):
    try:
        işlem=int(input("Yapmak istediğiniz işlemi seçiniz:")) #Sadece birden dörde kadar olan sayılar girilir 
        while(işlem<1 or işlem>4):                             
            işlem=int(input("Lütfen 1 ile 4 arasında bir sayı giriniz:"))
            break
    except ValueError:
        print("Lütfen sayı giriniz!")
    if(işlem==1):
        while(True):
            kullanıcı_adı=input("Kullanıcı adı belirleyiniz:") #Kullanıcı adı en az beş karakter olmalıdır
            if(len(kullanıcı_adı)<5):    
                print("Kullanıcı adı en az beş karakterden oluşmalıdır")
            else:
                print("Kullanıcı adınız geçerlidir")
                break
        eposta=input("E-posta adresinizi giriniz:") #Eposta adresi olabilmesi için "@" ve "." içermelidir
        while(True):
            if not(("@" in eposta) and ("." in eposta)):
                print("Üzgünüm bu geçerli bir e-posta adresi değildir")
                eposta=input("E-posta adresinizi giriniz:")
            else:
                print("E-postanız geçerlidir")
                break
        while(True):
            telefon_no=input("Bir iletişim numarası giriniz:") #Numara 11 haneli ve sayı içermelidir
            if(telefon_no.isdigit()) and (len(telefon_no)==11):
                print("Numaranız geçerlidir")
                break
            else:
                print("Lütfen geçerli bir değer giriniz")
        while(True):
            şifre=input("Bir şifre belirleyiniz:")
            şifre_tekrar=input("Şifrenizi tekrar giriniz:")
            if(şifre==şifre_tekrar):
                break
            else:
                print("Şifreler eşleşmiyor")
        print("Kayıt başarıyla oluşturuldu")
        
    elif(işlem==2):
        while(True):
            eposta_giriş=input("E-posta:")
            if(eposta_giriş==eposta):
                print("E-postanız doğru")
                break
            else:
                print("E-postanız yanlış tekrar giriniz")
        sayaç=0
        while(True):
            şifre_giriş=input("Şifre:") #Şifre en fazla 3 defa yanlış girileblir
            if(şifre_giriş==şifre):
                print("Şifreniz doğru\n")
                print("Giriş yapılıyor") 
                break
            else:
                sayaç+=1
                print("Şifreniz yanlış tekrar giriniz")
                print("Şifrenizi mi unuttunuz?")
                if(sayaç==3):
                    print("Şifreyi üçten fazla yanlış girdiğiniz için bloklandınız ")
                    break
      #işlem 2 ile ilgili yani giriş yaptıktan sonraki işlemler daha sonra buradan devam edecek                  
    elif(işlem==3):
        while(True):
            eposta_kontrol=input("E-posta adresinizi giriniz:")
            if(eposta_kontrol==eposta):
                print("E-posta adresinize bir doğrulama kodu gönderdik")
                input("Doğrulama kodunu girin")
                #Burası dosyalama konusunu görünce randit fonksiyonu ile daha detaylı yapılacak
                break  
            else:
                print("E-posta adresiniz yanlış")
    else:
        print("Çıkış yapılıyor")
        break
    
        
        
        
          
                 
                
                
       
       
    