
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Piyasa Mikroyapısı Laboratuvarı",
    page_icon="📈",
    layout="wide"
)

defaults = {
    "mission1_done": False,
    "mission2_done": False,
    "mission3_done": False,
    "score": 0,
    "student_note_1": "",
    "student_note_2": "",
    "student_note_3": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def build_order_book(mid_price, spread, depth_level, levels=5):
    tick = 0.10
    best_bid = round(mid_price - spread / 2, 2)
    best_ask = round(mid_price + spread / 2, 2)

    depth_map = {"Düşük": 400, "Orta": 1000, "Yüksek": 2500}
    base_qty = depth_map[depth_level]

    bids, asks = [], []
    for i in range(levels):
        bids.append({
            "Fiyat": round(best_bid - i * tick, 2),
            "Miktar": int(base_qty * (1 + 0.35 * i))
        })
        asks.append({
            "Fiyat": round(best_ask + i * tick, 2),
            "Miktar": int(base_qty * (1 + 0.35 * i))
        })

    return pd.DataFrame(bids), pd.DataFrame(asks)

def execute_market_order(book, order_qty):
    remaining = int(order_qty)
    executions = []

    for _, row in book.iterrows():
        if remaining <= 0:
            break
        qty = min(remaining, int(row["Miktar"]))
        executions.append((float(row["Fiyat"]), qty))
        remaining -= qty

    executed_qty = sum(q for _, q in executions)

    if executed_qty == 0:
        return {
            "executed_qty": 0,
            "remaining": order_qty,
            "vwap": np.nan,
            "last_price": np.nan,
            "executions": []
        }

    total_value = sum(p * q for p, q in executions)
    vwap = total_value / executed_qty

    return {
        "executed_qty": executed_qty,
        "remaining": remaining,
        "vwap": vwap,
        "last_price": executions[-1][0],
        "executions": executions
    }

def money(x):
    return f"{x:,.2f} TL".replace(",", "X").replace(".", ",").replace("X", ".")

def pct(x):
    return f"%{x*100:.3f}".replace(".", ",")

def progress_value():
    done = sum([
        st.session_state.mission1_done,
        st.session_state.mission2_done,
        st.session_state.mission3_done,
    ])
    return done / 3

def add_score_once(flag_name, points):
    if not st.session_state[flag_name]:
        st.session_state[flag_name] = True
        st.session_state.score += points

st.title("📈 Piyasa Mikroyapısı Laboratuvarı")
st.caption("Pay Piyasası, Emirler ve Piyasa Mikroyapısı | Uygulamalı sınıf çalışması")

st.markdown(
    """
Bu uygulamada amaç **doğru cevabı bulmaktan çok**, piyasa koşulları değiştiğinde
**spread, derinlik, price impact ve işlem maliyetlerinin nasıl birlikte değiştiğini görmek**.

Uygulama üç görevden oluşur.
"""
)

c1, c2 = st.columns([3, 1])
with c1:
    st.progress(progress_value())
with c2:
    st.metric("Puan", f"{st.session_state.score}/100")

st.divider()

st.header("Görev 1 — Aynı Emir, Farklı Piyasa")

st.markdown(
    """
Aynı büyüklükteki **piyasa emrini** iki farklı piyasa koşulunda çalıştırın.

Amaç:
- spread değişince ne oluyor?
- piyasa derinliği azalınca ne oluyor?
- VWAP ve slippage nasıl etkileniyor?
"""
)

colA, colB = st.columns(2)

with colA:
    st.subheader("Senaryo A")
    spread_a = st.select_slider(
        "Spread A (TL)",
        options=[0.10, 0.20, 0.40, 0.60, 1.00],
        value=0.20,
        key="spread_a"
    )
    depth_a = st.selectbox(
        "Derinlik A",
        ["Yüksek", "Orta", "Düşük"],
        index=0,
        key="depth_a"
    )

with colB:
    st.subheader("Senaryo B")
    spread_b = st.select_slider(
        "Spread B (TL)",
        options=[0.10, 0.20, 0.40, 0.60, 1.00],
        value=0.60,
        key="spread_b"
    )
    depth_b = st.selectbox(
        "Derinlik B",
        ["Yüksek", "Orta", "Düşük"],
        index=2,
        key="depth_b"
    )

mid_price = 100.0
order_qty = st.slider(
    "Her iki senaryoda piyasa alış emri büyüklüğü",
    min_value=500,
    max_value=8000,
    value=3000,
    step=500
)

_, ask_a = build_order_book(mid_price, spread_a, depth_a)
_, ask_b = build_order_book(mid_price, spread_b, depth_b)

res_a = execute_market_order(ask_a, order_qty)
res_b = execute_market_order(ask_b, order_qty)

best_ask_a = ask_a.iloc[0]["Fiyat"]
best_ask_b = ask_b.iloc[0]["Fiyat"]

slip_a = res_a["vwap"] - best_ask_a if res_a["executed_qty"] else np.nan
slip_b = res_b["vwap"] - best_ask_b if res_b["executed_qty"] else np.nan

if st.button("Senaryoları Karşılaştır", type="primary", key="compare_scenarios"):
    results = pd.DataFrame({
        "Gösterge": ["Spread", "Derinlik", "VWAP", "Slippage", "Gerçekleşen miktar"],
        "Senaryo A": [
            money(spread_a), depth_a, money(res_a["vwap"]),
            money(slip_a), f'{res_a["executed_qty"]} adet'
        ],
        "Senaryo B": [
            money(spread_b), depth_b, money(res_b["vwap"]),
            money(slip_b), f'{res_b["executed_qty"]} adet'
        ],
    })
    st.dataframe(results, use_container_width=True, hide_index=True)

    if slip_b > slip_a:
        st.success(
            "Senaryo B'de aynı emir daha yüksek slippage yaratıyor. "
            "Bu, sığ piyasa ve/veya geniş spread koşullarında işlem maliyetinin artabileceğini gösteriyor."
        )
    elif slip_b < slip_a:
        st.info(
            "Bu ayarlarda Senaryo A daha yüksek slippage yarattı. "
            "Hangi parametrenin sonucu değiştirdiğini kontrol edin."
        )
    else:
        st.info(
            "İki senaryo aynı slippage değerini üretti. "
            "Spread veya derinliği daha belirgin biçimde değiştirin."
        )

note1 = st.text_area(
    "Kısa yorumunuz: Aynı emir neden iki piyasada farklı sonuç üretti?",
    value=st.session_state.student_note_1,
    key="note1_widget"
)

if st.button("Görev 1'i Tamamla", key="finish1"):
    st.session_state.student_note_1 = note1
    if len(note1.strip()) < 20:
        st.warning("En az bir kısa gerekçe yazın.")
    else:
        add_score_once("mission1_done", 30)
        st.success("Görev 1 tamamlandı. +30 puan")

st.divider()

st.header("Görev 2 — İşlem Maliyeti Nereden Geliyor?")

st.markdown(
    """
Aşağıdaki işlem için **quoted spread, effective spread, realized spread ve price impact**
hesaplamalarını inceleyin.
"""
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    bid = st.number_input("Bid", value=99.80, step=0.10)
with c2:
    ask = st.number_input("Ask", value=100.20, step=0.10)
with c3:
    trade_price = st.number_input("İşlem fiyatı", value=100.20, step=0.10)
with c4:
    future_mid = st.number_input("İşlem sonrası orta fiyat", value=100.10, step=0.10)

mid = (bid + ask) / 2
q = 1

quoted_spread = ask - bid
effective_spread = 2 * q * (trade_price - mid)
realized_spread = 2 * q * (trade_price - future_mid)
price_impact = 2 * q * (future_mid - mid)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Quoted spread", money(quoted_spread))
m2.metric("Effective spread", money(effective_spread))
m3.metric("Realized spread", money(realized_spread))
m4.metric("Price impact", money(price_impact))

st.caption(
    f"Kontrol: Effective Spread = Realized Spread + Price Impact → "
    f"{effective_spread:.2f} = {realized_spread:.2f} + {price_impact:.2f}"
)

q2 = st.radio(
    "Bu örnekte price impact yüksekse en doğru yorum hangisidir?",
    [
        "İşlem sonrası orta fiyat, işlem öncesine göre daha fazla değişmiştir.",
        "Spread mutlaka sıfırdır.",
        "Piyasa derinliği mutlaka sonsuzdur.",
        "İşlem maliyeti yoktur."
    ],
    index=None
)

note2 = st.text_area(
    "Kısa yorumunuz: Effective spread ile price impact arasındaki farkı kendi cümlenizle açıklayın.",
    value=st.session_state.student_note_2,
    key="note2_widget"
)

if st.button("Görev 2'yi Tamamla", key="finish2"):
    st.session_state.student_note_2 = note2
    correct = q2 == "İşlem sonrası orta fiyat, işlem öncesine göre daha fazla değişmiştir."
    note_ok = len(note2.strip()) >= 20

    if not correct:
        st.warning("Çoktan seçmeli yanıtı tekrar değerlendirin.")
    elif not note_ok:
        st.warning("Kısa açıklamanızı biraz daha geliştirin.")
    else:
        add_score_once("mission2_done", 30)
        st.success("Görev 2 tamamlandı. +30 puan")

st.divider()

st.header("Görev 3 — Likidite mi, Bilgi mi?")

st.markdown(
    """
Bir payda aynı gün şu gelişmeler gözleniyor:

- spread genişliyor,
- emir defteri derinliği azalıyor,
- Kyle λ yükseliyor,
- büyük işlemler fiyatı daha fazla hareket ettiriyor,
- birkaç dakika sonra emir defteri kısmen toparlanıyor,
- şirket hakkında doğrulanmış yeni bir haber yok.

Bu tabloyu birlikte yorumlayın.
"""
)

q3a = st.radio(
    "1. En doğrudan hangi sonuç destekleniyor?",
    [
        "Piyasa likiditesi bozulmuştur.",
        "Şirketin temel değeri kesin olarak düşmüştür.",
        "Piyasa tamamen etkin hale gelmiştir.",
        "İşlem maliyetleri ortadan kalkmıştır."
    ],
    index=None
)

q3b = st.radio(
    "2. Kyle λ'nın yükselmesi neyi gösterir?",
    [
        "Emir akışının fiyat üzerindeki etkisinin arttığını",
        "Spread'in sıfırlandığını",
        "Settlement süresinin uzadığını",
        "Emirlerin artık eşleşmediğini"
    ],
    index=None
)

q3c = st.radio(
    "3. Fiyatın daha sonra kısmen geri dönmesi hangi yorumu destekler?",
    [
        "Hareketin bir bölümünün geçici likidite etkisi olabileceğini",
        "Bütün hareketin kesin olarak özel bilgiden kaynaklandığını",
        "Piyasanın sonsuz derinliğe sahip olduğunu",
        "Quoted spread'in anlamsız olduğunu"
    ],
    index=None
)

note3 = st.text_area(
    "Son yorum: Bu vakada neden yalnızca fiyat değişimine bakmak yeterli değildir?",
    value=st.session_state.student_note_3,
    key="note3_widget"
)

if st.button("Görev 3'ü Tamamla", key="finish3"):
    st.session_state.student_note_3 = note3
    correct = all([
        q3a == "Piyasa likiditesi bozulmuştur.",
        q3b == "Emir akışının fiyat üzerindeki etkisinin arttığını",
        q3c == "Hareketin bir bölümünün geçici likidite etkisi olabileceğini",
    ])
    note_ok = len(note3.strip()) >= 20

    if not correct:
        st.warning("Yanıtlarınızdan en az biri hatalı. Kavramları birlikte değerlendirin.")
    elif not note_ok:
        st.warning("Son yorumunuzu biraz daha geliştirin.")
    else:
        add_score_once("mission3_done", 40)
        st.success("Görev 3 tamamlandı. +40 puan")

st.divider()

st.header("🎯 Uygulama Sonucu")

done_count = sum([
    st.session_state.mission1_done,
    st.session_state.mission2_done,
    st.session_state.mission3_done,
])

st.write(f"Tamamlanan görev: **{done_count}/3**")
st.write(f"Toplam puan: **{st.session_state.score}/100**")

if st.session_state.score == 100:
    st.success(
        "Tüm görevler tamamlandı. Spread, derinlik, işlem maliyeti ve price impact kavramlarını birlikte yorumlayabiliyorsunuz."
    )
elif st.session_state.score >= 60:
    st.info(
        "Temel çerçeve güçlü. Eksik kalan görevi tamamlayarak kavramlar arasındaki bağlantıyı güçlendirin."
    )
else:
    st.warning(
        "Görevleri tamamladıkça uygulama size kavramlar arasındaki ilişkiyi adım adım gösterecek."
    )

summary_text = f"""
PİYASA MİKROYAPISI LABORATUVARI

Puan: {st.session_state.score}/100

GÖREV 1 YORUMU
{st.session_state.student_note_1}

GÖREV 2 YORUMU
{st.session_state.student_note_2}

GÖREV 3 YORUMU
{st.session_state.student_note_3}
"""

st.download_button(
    "Kendi Yanıtlarımı İndir",
    data=summary_text.encode("utf-8"),
    file_name="piyasa_mikroyapisi_uygulama_yanitlari.txt",
    mime="text/plain"
)

st.caption(
    "Ders uygulaması | Pay Piyasası, Emirler ve Piyasa Mikroyapısı | "
    "Hesaplamalar öğretim amaçlıdır."
)
