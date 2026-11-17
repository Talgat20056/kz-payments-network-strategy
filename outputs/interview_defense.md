# Interview defence — the 10 hardest questions

Format for each: **Q** → short answer → **the weakest point, which I must not overclaim**. Source keys are listed in `outputs/findings.md`.

---

**1. "You call the local system 'Kaspi'. How do you know the 77% is Kaspi?"**
NBK's release narrative says cards are issued for international systems "as well as payment cards of the local system Kaspi.kz" (NBK-277 text). The tables only say "local systems". Kaspi's own disclosures are consistent with this. Kaspi QR+card TPV of ₸30.5trn [calc, K25 p92] equals 82% of NBK POS+QR value.
*Weakest point:* I cannot prove that 100% of "local systems" is Kaspi, or that every Kaspi Gold transaction is booked as local rather than Visa. Kaspi recognises revenue as an agent "when using third-party payments platforms or networks (e.g., Visa/Mastercard)" (K25 p181), so some Kaspi volume does touch networks. Say "the local system (Kaspi.kz per NBK)", never "Kaspi's 77%".

**2. "What is a 'used' card? Isn't dormancy just people holding several cards, or virtual cards?"**
NBK does not publish the definition. There are 85.4m cards for a population of 20.6m [calc; NBK-277 T1, STAT], about 4 per person, so a lot of dormancy is structural (secondary, virtual, or replacement cards).
*Weakest point:* the 32.3m dormant cards are a ceiling, not an addressable market. That is why the sizing uses only +2/+5/+10pp of activation and an α of 15–40% of average spend. Never say "₸X trillion locked in dormant cards".

**3. "H3 'killed' on 12–24 months of data? Couldn't the share drop be reclassification or a pricing change?"**
Possibly. Kaspi increased "monetized P2P transactions" revenue (K25 p104), which may have pushed some free P2P off the local rail. A bank re-badging its card base would also move the split. Two independent signals point the same way, though: local share fell (−1.8pp FY, −1.4pp YoY 9M) and QR's in-store share plateaued (~52%).
*Weakest point:* this is a short series. Frame it as "the closed loop has stopped gaining", not "networks are winning back share".

**4. "Isn't cross-border growth just macro (travel, tenge, Chinese marketplaces)? What does a network's investment change?"**
Yes. Demand growth (+25.6% CNP abroad, NBK-277 T7) is market-driven, and I make no causal claim that networks created it. Network investment changes *capture*: authorisation rates, tokenised credentials, fraud and 3-DS friction, and pricing transparency.
*Weakest point:* I have no authorisation-rate or fraud data, so the "capture" upside is unquantified. KPI #1 tracks market growth; a network would add its own approval-rate KPI internally.

**5. "How will Kaspi respond?"**
It is already moving: AliPay+ integration for inbound and outbound wallets (K25 p53, p58), QR interoperability with 7 local banks and 1 Kyrgyz bank (K25 p58), Kaspi Alaqan pay-by-palm (launched Dec 2025, K25 p53), and continued QR migration to avoid interchange (K25 p105). Its most dangerous counter is an outbound wallet via AliPay+ that substitutes for cards at foreign merchants.
*Weakest point:* recommendation #1 assumes card credentials stay the default for foreign e-commerce. If AliPay+-style wallets reach KZ consumers at scale, the "structural" niche narrows. I cannot size that risk from public data.

**6. "What role does the regulator play?"**
NBK sets payment-system rules and publishes this data. Kaspi Bank has been on the Register of Significant Payment Services Providers since 2018. One qualifying threshold is processing ≥ 25% of card payment volume (K25 p66), which brings extra NBK reporting and risk requirements. Interoperability (QR across banks) and any interchange rules are NBK levers that could move the domestic battlefield either way.
*Weakest point:* I did not analyse NBK policy documents (QR standards, interchange, data localisation). Recommendation #3's "engage NBK" is a direction, not a forecast of what NBK will do.

**7. "You talk volume. How does this become network revenue?"**
Public data gives value and counts, not fees. Network revenue per tenge differs by flow: cross-border carries extra fees versus domestic, and cash withdrawals earn little. So the direction of the recommendations is robust, but I do not translate into revenue.
*Weakest point:* no fee or yield data. Never quote a revenue number. If pressed, say I would use the client's own yield curve by flow type.

**8. "Your 66% bypass number depends on s, which you made up."**
Correct, which is why it is labelled [estimate] with a range of 49–76%. The conclusion that "about half or more of in-store value bypasses networks" holds across the whole range. The *trend* conclusion does not use this estimate; it rests on the [calc] local share (T4/T7) and the QR share (T6).
*Weakest point:* the estimate's flat trend is partly by construction (s is held constant). Never cite it as evidence of stability. The anchors for s are weak: local cards are 42% of used cards (T1), and Kaspi says other cards' POS volumes are "significantly lower" (K25 p91).

**9. "Inbound fell 5%. Is that real?"**
It is a residual: T6 − (T4 − T7). Each table is revised by about 0.1% between vintages, and T5 and T6 differ by up to ~0.3% despite the same stated scope (`docs/validation_nbk.md`). On a ₸140trn base that noise (~₸0.2–0.4trn) is the same size as the inbound change.
*Weakest point:* inbound "flat" is defensible; inbound "declining" is not. No scheme split exists.

**10. "Why dismiss credit? BNPL and credit are the biggest profit pools in Kazakhstan."**
That is exactly why: the profit pool sits in the closed loop. Of 13.0m credit cards, 92% are on the local system [calc; NBK-277 T1/T2], and Kaspi's BNPL is native to its super app. A network credit play would need a non-Kaspi issuer with underwriting scale to take share in Kaspi's strongest product.
*Weakest point:* the credit-card *count* is not credit *volume*. NBK does not split transaction value by card type × scheme. Also, local credit is a residual (T2 credit − T1 international credit), so it assumes T1 and T2 classify card types the same way.

---

## Things I must not say
- "Kaspi has 77% share." Say instead: the local system (named by NBK as Kaspi.kz) handles 77% of *KZ-card domestic cashless value incl. P2P*.
- "E-commerce in Kazakhstan is ₸X." Not separable in NBK data; "internet & mobile" includes P2P.
- "Networks are winning back share." The data supports only "the closed loop has stopped gaining".
- Any revenue or fee figure.
- Any number from the 2023-H1 block of release v250 or Table 1 of release v263 (source errors; see `docs/data_gaps.md`).
