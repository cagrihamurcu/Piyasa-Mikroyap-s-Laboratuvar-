
import streamlit as st

st.set_page_config(
    page_title="Piyasa Mikroyapısı Uygulaması",
    page_icon="📈",
    layout="centered"
)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
for key, default in {
    "puan": 0,
    "g1": False,
    "g2": False,
    "g3": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def add_points(flag, points):
    if not st.session_state[flag]:
        st.session_state[flag] = True
        st.session_state.puan += points


# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("📈 Piyasa Mikroyapısı Uygulaması")

st.write(
    """
Bu uygulamada amaç, derste gördüğümüz kavramları kısa örneklerle
**görmek, yorumlamak ve birbirine bağlamaktır.**

Uygulama üç kısa görevden oluşur.
"""
)

done = sum([st.session_state.g1, st.session_state.g2, st.session_state.g3])
st.progress(done / 3)
st.metric("Puan", f"{st.session_state.puan}/100")

st.divider()

# =================================================
# GÖREV 1
# =================================================
st.header("🎯 Görev 1 — Spread ve Piyasa Derinliği")

st.subheader("Önce kavramları hatırlayalım")

st.markdown(
    """
**Spread nedir?**  
En iyi alış fiyatı ile en iyi satış fiyatı arasındaki farktır.

- **Dar spread:** alış ve satış fiyatları birbirine daha yakındır.
- **Geniş spread:** alış ve satış fiyatları birbirinden daha uzaktır.

**Piyasa derinliği nedir?**  
Farklı fiyat seviyelerinde ne kadar alış ve satış emri bulunduğunu gösterir.

- **Derin piyasa:** daha fazla alış ve satış emri vardır.
- **Sığ piyasa:** daha az alış ve satış emri vardır.

**Önemli:**  
Dar spread tek başına yüksek likidite anlamına gelmez.
"""
)

st.subheader("Şimdi karşılaştıralım")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
### Piyasa A
- Spread **dar**
- Piyasa derinliği **yüksek**
"""
    )

with col2:
    st.markdown(
        """
### Piyasa B
- Spread **geniş**
- Piyasa derinliği **düşük**
"""
    )

st.write(
    """
Aynı büyüklükte büyük bir **piyasa alış emri** iki piyasaya da gönderiliyor.

Sizce hangi piyasada fiyat daha fazla hareket edebilir?
"""
)

q1 = st.radio(
    "Seçiminiz:",
    ["Piyasa A", "Piyasa B"],
    index=None,
    key="q1"
)

if st.button("Cevabı kontrol et", key="check1"):
    if q1 == "Piyasa B":
        st.success("✅ Doğru")
        st.markdown(
            """
Piyasa B daha sığdır.

Piyasa derinliği düşük olduğunda büyük bir piyasa emri mevcut emirleri daha hızlı tüketebilir
ve işlem farklı fiyat seviyelerinden gerçekleşebilir.

**Temel fikir:**  
👉 Piyasa derinliği azaldıkça büyük emirlerin fiyat etkisi artabilir.
"""
        )
        add_points("g1", 30)

    elif q1 == "Piyasa A":
        st.warning("Bir kez daha düşünün.")
        st.write(
            "Derin piyasa, büyük emirleri daha sınırlı fiyat hareketiyle karşılayabilir."
        )
    else:
        st.info("Önce bir seçenek işaretleyin.")

st.divider()

# =================================================
# GÖREV 2
# =================================================
st.header("💸 Görev 2 — Spread Ne Anlatır?")

st.subheader("Önce kavramları hatırlayalım")

st.markdown(
    """
**Bid:** piyasadaki en yüksek alış fiyatıdır.  
**Ask:** piyasadaki en düşük satış fiyatıdır.

**Spread = Ask − Bid**

Spread yalnızca iki fiyat arasındaki fark değildir.

Aynı zamanda piyasanın:

- işlem maliyeti,
- likiditesi,
- bilgi ve risk düzeyi

hakkında fikir verebilir.
"""
)

st.subheader("Kısa örnek")

st.markdown(
    """
- **Bid = 99,80 TL**
- **Ask = 100,20 TL**
"""
)

if st.button("Spread'i göster", key="spread_calc"):
    st.info("Spread = 100,20 − 99,80 = **0,40 TL**")

st.write("Şimdi yorumlayalım.")

q2 = st.radio(
    "Spread genişlediğinde genel olarak hangi yorum daha uygundur?",
    [
        "İşlem maliyeti artabilir ve likidite azalabilir.",
        "Şirketin temel değeri kesin olarak artmıştır.",
        "Piyasa mutlaka daha derindir."
    ],
    index=None,
    key="q2"
)

if st.button("Yorumu kontrol et", key="check2"):
    if q2 == "İşlem maliyeti artabilir ve likidite azalabilir.":
        st.success("✅ Doğru")
        st.markdown(
            """
Spread genişlediğinde alış ve satış fiyatları birbirinden uzaklaşır.

Bu durum, işlem yapmanın daha maliyetli hale geldiğine ve likiditenin zayıflayabileceğine işaret edebilir.

**Temel fikir:**  
👉 Spread, işlem maliyeti ve likidite hakkında bilgi verir.
"""
        )
        add_points("g2", 30)

    elif q2:
        st.warning("Bu yorum dersteki çerçeveyle uyumlu değil.")
        st.write(
            "Spread, şirketin temel değerini tek başına göstermez; daha çok işlem koşullarıyla ilgilidir."
        )
    else:
        st.info("Önce bir seçenek işaretleyin.")

st.divider()

# =================================================
# GÖREV 3
# =================================================
st.header("🧠 Görev 3 — Bilgi Şoku mu, Likidite Şoku mu?")

st.subheader("Önce kavramları hatırlayalım")

st.markdown(
    """
**Bilgi şoku:**  
Şirketle ilgili yeni bilgi gelir ve yatırımcıların değerleme beklentisi değişir.

**Likidite şoku:**  
Şirketle ilgili yeni bilgi olmadan büyük alış veya satış baskısı oluşur.

Likidite şokuna örnek:

- fon çıkışları,
- portföy yeniden dengelemesi,
- teminat ihtiyacı.
"""
)

st.subheader("Vaka")

st.markdown(
    """
Bir payın fiyatı kısa sürede düşüyor.

Aynı anda:

- spread genişliyor,
- piyasa derinliği azalıyor,
- büyük satışlar fiyatı daha fazla hareket ettiriyor,
- bir süre sonra fiyatın bir kısmı geri geliyor,
- şirket hakkında yeni bir haber bulunmuyor.
"""
)

q3 = st.radio(
    "Bu tablo için en uygun ilk yorum hangisidir?",
    [
        "Likidite şoku yaşanmış olabilir.",
        "Şirketin temel değeri kesin olarak düşmüştür.",
        "Fiyat hareketinin tamamı yeni bilgiden kaynaklanmıştır."
    ],
    index=None,
    key="q3"
)

if st.button("Vakayı kontrol et", key="check3"):
    if q3 == "Likidite şoku yaşanmış olabilir.":
        st.success("✅ Doğru")
        st.markdown(
            """
Şirket hakkında yeni bilgi olmadan büyük satış baskısı oluşması,
likidite şoku ile uyumludur.

Fiyatın daha sonra kısmen geri dönmesi de hareketin bir bölümünün
geçici likidite etkisi taşıyabileceğini düşündürür.

**Temel fikir:**  
👉 Her fiyat hareketi yeni bilgi anlamına gelmez.
"""
        )
        add_points("g3", 40)

    elif q3:
        st.warning("Bu kadar kesin bir sonuca varamayız.")
        st.write(
            "Fiyatın düşmesi tek başına bunun bilgi şokundan kaynaklandığını göstermez."
        )
    else:
        st.info("Önce bir seçenek işaretleyin.")

st.divider()

# =================================================
# SONUÇ
# =================================================
st.header("🏁 Sonuç")

if st.session_state.puan == 100:
    st.balloons()
    st.success("Tebrikler! Tüm görevleri tamamladınız. 🎉")
    st.markdown(
        """
Bugünün üç ana mesajı:

1. **Piyasa derinliği azaldıkça büyük emirlerin fiyat etkisi artabilir.**
2. **Spread, işlem maliyeti ve likidite hakkında bilgi verir.**
3. **Her fiyat hareketi yeni bilgi anlamına gelmez.**
"""
    )
elif st.session_state.puan >= 60:
    st.info("Gayet iyi gidiyorsunuz. Kalan görevi de tamamlayın.")
else:
    st.write("Görevleri tamamladıkça puanınız artacak.")

st.caption(
    "Ders uygulaması — Pay Piyasası, Emirler ve Piyasa Mikroyapısı"
)
