            result = execute_market_order(bid_book, order_qty)
            benchmark = bid_book.iloc[0]['Fiyat']
            slippage = benchmark - result['vwap'] if result['executed_qty'] else np.nan
            price_impact = mid_price - result['last_price'] if result['executed_qty'] else np.nan

        if result['executed_qty'] == 0:
            st.error('Emir gerçekleştirilemedi.')
        else:
            relative_spread = spread / mid_price
            m1, m2, m3, m4 = st.columns(4)
            m1.metric('Gerçekleşen miktar', f"{result['executed_qty']:,} adet".replace(',', '.'))
            m2.metric('VWAP', money(result['vwap']))
            m3.metric('Slippage', money(slippage))
            m4.metric('Son fiyat etkisi', money(price_impact))

            exec_df = pd.DataFrame(result['executions'], columns=['Gerçekleşme fiyatı','Miktar'])
            exec_df['İşlem tutarı'] = exec_df['Gerçekleşme fiyatı'] * exec_df['Miktar']
            st.dataframe(exec_df, use_container_width=True, hide_index=True)

            if result['remaining'] > 0:
                st.warning(f"Emrin {result['remaining']:,} adedi görünür emir defterinde karşılanamadı.".replace(',', '.'))

            if slippage <= 0.05:
                st.success('Emir mevcut likidite tarafından sınırlı fiyat etkisiyle karşılandı.')
            elif slippage <= 0.30:
                st.info('Emir birden fazla fiyat kademesini tüketti.')
            else:
                st.warning('Emir önemli ölçüde likidite tüketti; fiyat riski yükseldi.')

            st.write(f'Quoted spread: **{money(spread)}** | Relative spread: **{pct(relative_spread)}**')

    st.markdown('''
#### Grup görevi
Aynı emir büyüklüğünü koruyarak yalnızca **spread** ve **piyasa derinliğini** değiştirin.

1. Hangi koşulda VWAP ve slippage daha fazla bozuldu?
2. Bulgularınız **“dar spread tek başına yüksek likidite anlamına gelmez”** ifadesini destekliyor mu?
''')

with tab2:
    st.header('2. Mikroyapı Ölçümleri')
    st.subheader('A. Spread ve Price Impact')

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        bid = st.number_input('Bid', value=99.80, step=0.10, key='m_bid')
    with c2:
        ask = st.number_input('Ask', value=100.20, step=0.10, key='m_ask')
    with c3:
        trade_price = st.number_input('İşlem fiyatı', value=100.20, step=0.10)
    with c4:
        future_mid = st.number_input('İşlem sonrası orta fiyat', value=100.10, step=0.10)

    trade_direction = st.radio('İşlem yönü', ['Alıcı başlatmalı','Satıcı başlatmalı'], horizontal=True)
    mid = (bid + ask)/2
    q = 1 if trade_direction == 'Alıcı başlatmalı' else -1
    quoted_spread = ask - bid
    relative_spread = quoted_spread / mid
    effective_spread = 2*q*(trade_price-mid)
    realized_spread = 2*q*(trade_price-future_mid)
    price_impact = 2*q*(future_mid-mid)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric('Quoted spread', money(quoted_spread))
    m2.metric('Relative spread', pct(relative_spread))
    m3.metric('Effective spread', money(effective_spread))
    m4.metric('Price impact', money(price_impact))
    st.write(f'Realized spread: **{money(realized_spread)}**')
    st.write(f'Kontrol: **Effective Spread = Realized Spread + Price Impact** → {effective_spread:.2f} = {realized_spread:.2f} + {price_impact:.2f}')

    st.divider()
    st.subheader('B. Kyle λ')
    order_flow = st.number_input('Net emir akışı Q (adet)', min_value=100, value=5000, step=500)
    price_change = st.number_input('Fiyat değişimi ΔP (TL)', value=0.50, step=0.05)
    kyle_lambda = price_change / order_flow
    st.metric('Yaklaşık Kyle λ', f'{kyle_lambda:.6f} TL/adet')
    st.caption('Not: Bu oran öğretim amaçlı sezgisel bir gösterimdir; ampirik Kyle λ genellikle regresyon temelli tahmin edilir.')

    st.divider()
    st.subheader('C. Amihud ILLIQ')
    col1, col2 = st.columns(2)
    with col1:
        abs_return = st.number_input('Mutlak günlük getiri', min_value=0.0001, max_value=0.20, value=0.015, step=0.001, format='%.4f')
    with col2:
        tl_volume = st.number_input('Parasal işlem hacmi (TL)', min_value=100000.0, value=20000000.0, step=1000000.0)
    illiq = abs_return / tl_volume
    st.metric('Amihud ILLIQ', f'{illiq:.10f}')
    st.caption('ILLIQ yükseldikçe belirli işlem hacmine karşılık daha büyük fiyat hareketi gözlenir. Ölçü, likiditenin tamamını değil belirli bir illikidite boyutunu temsil eder.')

with tab3:
    st.header('3. Analitik Vaka')
    st.markdown('''
Bir payda gün içinde şu gelişmeler gözleniyor:

- quoted spread belirgin biçimde genişliyor,
- emir defteri derinliği azalıyor,
- büyük işlemler sonrasında fiyat daha fazla hareket ediyor,
- kısa süre içinde yeni emirler geliyor ve piyasa kısmen toparlanıyor,
- aynı gün şirket hakkında doğrulanmış yeni bir haber bulunmuyor.
''')

    q1 = st.radio('1. Bu bulgular en doğrudan hangi duruma işaret eder?', ['Likiditenin bozulmasına','Şirketin temel değerinin kesin olarak düşmesine','Piyasanın tamamen etkin hale gelmesine','Spread’in ekonomik anlamını kaybetmesine'], index=None)
    q2 = st.radio('2. Büyük işlemlerden sonra fiyatın daha fazla hareket etmesi hangi kavramla en yakından ilişkilidir?', ['Price impact','Settlement','Queue position','Order processing cost'], index=None)
    q3 = st.radio('3. Fiyatın daha sonra kısmen geri dönmesi hangi yorumu destekler?', ['Fiyat hareketinin en azından bir bölümünün geçici likidite etkisi taşıyabileceğini','Bütün fiyat hareketinin kesin olarak özel bilgiden kaynaklandığını','Likiditenin tamamen ortadan kalktığını','Bid ve ask fiyatlarının aynı olduğunu'], index=None)
    q4 = st.radio('4. Hangi yaklaşım doğrudan order flow ve price impact ilişkisine odaklanır?', ['Kyle','Grossman–Stiglitz','Roll','Demsetz'], index=None)

    if st.button('Yanıtları Değerlendir', type='primary'):
        answers = [
            q1 == 'Likiditenin bozulmasına',
            q2 == 'Price impact',
            q3 == 'Fiyat hareketinin en azından bir bölümünün geçici likidite etkisi taşıyabileceğini',
            q4 == 'Kyle'
        ]
        score = sum(answers)
        st.subheader(f'Sonuç: {score}/4')
        if score == 4:
            st.success('Tüm yanıtlar doğru.')
        elif score >= 2:
            st.info('Genel çerçeve doğru; bazı kavramları yeniden karşılaştırın.')
        else:
            st.warning('Spread, depth, price impact ve geçici/kalıcı fiyat etkisi bölümlerini yeniden gözden geçirin.')

        st.markdown('''
**Vakanın temel yorumu:** Bu bulgular tek başına şirketin temel değerinin değiştiğini göstermez. Spread’in genişlemesi, depth’in azalması ve price impact’in yükselmesi birlikte **piyasa likiditesinin bozulduğuna** işaret edebilir. Fiyatın daha sonra kısmen geri dönmesi ise hareketin en azından bir bölümünün **geçici likidite etkisi** olabileceğini düşündürür.
''')

st.divider()
st.caption('Ders uygulaması | Pay Piyasası, Emirler ve Piyasa Mikroyapısı | Hesaplamalar öğretim amaçlıdır.')
