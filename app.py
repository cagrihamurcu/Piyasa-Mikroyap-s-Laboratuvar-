
import streamlit as st

st.set_page_config(
    page_title="Piyasa Mikroyapısı Oyunu",
    page_icon="📊",
    layout="centered"
)

def tl(x):
    return f"{x:.2f} TL".replace(".", ",")

if "puan" not in st.session_state:
    st.session_state.puan = 0
if "g1" not in st.session_state:
    st.session_state.g1 = False
if "g2" not in st.session_state:
    st.session_state.g2 = False
if "g3" not in st.session_state:
    st.session_state.g3 = False

st.title("📊 Piyasa Mikroyapısı Oyunu")
st.write(
    """
Bu uygulamada amaç **formül ezberlemek değil**.

Amaç, bir emrin piyasada ne yaptığını **görerek ve deneyerek** öğrenmek.

Toplam 3 kısa görev var.
"""
)

tamamlanan = sum([st.session_state.g1, st.session_state.g2, st.session_state.g3])
st.progress(tamamlanan / 3)
st.metric("Toplam Puan", f"{st.session_state.puan}/100")

st.divider()

st.header("🎯 Görev 1 — Hangi Piyasa Daha Rahat?")

st.write(
    """
Aynı büyüklükte bir **piyasa alış emri** iki farklı piyasaya gönderiliyor.

**Piyasa A**
- Spread dar
- Emir defteri derin

**Piyasa B**
- Spread geniş
- Emir defteri sığ

Sizce büyük emir hangi piyasada fiyatı daha fazla hareket ettirir?
"""
)

cevap1 = st.radio(
    "Seçiminiz:",
    ["Piyasa A", "Piyasa B"],
    index=None,
    key="cevap1"
)

if st.button("Cevabı Göster", key="btn1"):
    if cevap1 == "Piyasa B":
        st.success("✅ Doğru!")
        st.write(
            """
Sığ piyasada karşı tarafta daha az emir vardır.

Büyük piyasa emri mevcut emirleri daha hızlı tüketir ve daha kötü fiyatlara doğru ilerleyebilir.

**Öğrenilen fikir:**  
👉 Derinlik azaldıkça büyük emrin fiyat etkisi artabilir.
"""
        )
        if not st.session_state.g1:
            st.session_state.g1 = True
            st.session_state.puan += 30
    elif cevap1 == "Piyasa A":
        st.warning("Bir kez daha düşünün.")
        st.write("Derin piyasa, büyük emirleri daha az fiyat hareketiyle karşılayabilir.")
    else:
        st.info("Önce bir seçenek işaretleyin.")

st.divider()

st.header("💸 Görev 2 — Spread Ne Anlatıyor?")

st.write(
    """
Bir pay için:

- **Bid = 99,80 TL**
- **Ask = 100,20 TL**

Önce spread'i hesaplayalım.
"""
)

bid = 99.80
ask = 100.20
spread = ask - bid

if st.button("Spread'i Hesapla", key="btn2calc"):
    st.info(f"Spread = Ask − Bid = **{tl(spread)}**")

cevap2 = st.radio(
    "Spread'in genişlemesi genellikle neyi gösterir?",
    [
        "İşlem maliyetinin ve likidite riskinin artabileceğini",
        "Piyasanın kesin olarak daha likit olduğunu",
        "Şirket değerinin kesin olarak arttığını"
    ],
    index=None,
    key="cevap2"
)

if st.button("Yorumu Kontrol Et", key="btn2"):
    if cevap2 == "İşlem maliyetinin ve likidite riskinin artabileceğini":
        st.success("✅ Doğru!")
        st.write(
            """
Spread yalnızca iki fiyat arasındaki fark değildir.

Aynı zamanda piyasanın işlem maliyeti ve likiditesi hakkında bilgi verir.

**Öğrenilen fikir:**  
👉 Spread genişledikçe işlem yapmak genellikle daha pahalı hale gelir.
"""
        )
        if not st.session_state.g2:
            st.session_state.g2 = True
            st.session_state.puan += 30
    elif cevap2:
        st.warning("Bu yorum fazla kesin.")
        st.write("Spread doğrudan şirketin temel değerini göstermez; daha çok işlem koşullarıyla ilgilidir.")
    else:
        st.info("Önce bir seçenek işaretleyin.")

st.divider()

st.header("🧠 Görev 3 — Bilgi mi, Likidite mi?")

st.write(
    """
Bir payda aynı anda şu gelişmeler oluyor:

- spread genişliyor,
- piyasa derinliği azalıyor,
- büyük işlemler fiyatı daha fazla hareket ettiriyor,
- bir süre sonra fiyatın bir kısmı geri geliyor,
- şirket hakkında yeni bir haber yok.

Bu durumda ilk akla gelmesi gereken nedir?
"""
)

cevap3 = st.radio(
    "Seçiminiz:",
    [
        "Likidite geçici olarak bozulmuş olabilir",
        "Şirketin temel değeri kesin olarak düşmüştür",
        "Piyasa tamamen etkin hale gelmiştir"
    ],
    index=None,
    key="cevap3"
)

if st.button("Vakayı Çöz", key="btn3"):
    if cevap3 == "Likidite geçici olarak bozulmuş olabilir":
        st.success("✅ Doğru!")
        st.write(
            """
Yeni haber yoksa ve fiyat daha sonra kısmen geri dönüyorsa,
hareketin bir kısmı **geçici likidite etkisi** olabilir.

**Öğrenilen fikir:**  
👉 Her fiyat hareketi yeni bilgi anlamına gelmez.
"""
        )
        if not st.session_state.g3:
            st.session_state.g3 = True
            st.session_state.puan += 40
    elif cevap3:
        st.warning("Bu sonuç için yeterli kanıt yok.")
        st.write("Tek başına fiyat düşüşü, şirketin temel değerinin değiştiğini kanıtlamaz.")
    else:
        st.info("Önce bir seçenek işaretleyin.")

st.divider()

st.header("🏁 Sonuç")

if st.session_state.puan == 100:
    st.balloons()
    st.success("Tebrikler! 3 görevi de tamamladınız. 🎉")
    st.write(
        """
Bugünün 3 ana mesajı:

1. **Derinlik azaldıkça büyük emirlerin fiyat etkisi artabilir.**
2. **Spread, işlem maliyeti ve likidite hakkında bilgi verir.**
3. **Her fiyat hareketi yeni bilgi anlamına gelmez.**
"""
    )
elif st.session_state.puan >= 60:
    st.info("Gayet iyi gidiyorsunuz. Kalan görevi de tamamlayın.")
else:
    st.write("Görevleri tamamladıkça puanınız artacak.")

st.caption("Ders uygulaması — Pay Piyasası, Emirler ve Piyasa Mikroyapısı")
