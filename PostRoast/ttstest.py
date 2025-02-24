import asyncio
import edge_tts

async def metni_seslendir(metin, ses_profili, cikti_dosyasi):
   
    try:
        communicate = edge_tts.Communicate(metin, voice=ses_profili)
        await communicate.save(cikti_dosyasi)
        print(f"Ses dosyası başarıyla oluşturuldu: {cikti_dosyasi}")
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    metin = input("Seslendirmek istediğiniz metni girin: ")
    ses_profili = "tr-TR-EmelNeural"  # Kullanmak istediğiniz ses profilini girin.
    cikti_dosyasi = "seslendirme.mp3"  # Çıktı dosyasının adını ve yolunu ayarlayın.

    asyncio.run(metni_seslendir(metin, ses_profili, cikti_dosyasi))