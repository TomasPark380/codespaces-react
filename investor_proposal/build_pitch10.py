"""PHYDRION 마중물 투자 제안서 — 10장 압축판.

사용법:
    python build_pitch10.py   # → PHYDRION_Pitch_10p.pdf

그리기 도구와 일부 페이지는 build_proposal.py, 모든 수치는 model.py 에서 가져온다.
"""

import os

from reportlab.lib.colors import HexColor, white

import model as M
from build_proposal import (B, CARD, GOLD, GOLD_BG, HERE, INK, LINE, MUTED, NAVY, NAVY2, NOTE_TARGET, R,
                            SERIES, TEAL, TEAL_D, XB, Deck, H, W, p_hook, p_priming, register_fonts)

OUT = os.path.join(HERE, "PHYDRION_Pitch_10p.pdf")
SOFT = HexColor("#c9d6e3")


def cover(d):
    d.page_no += 1
    base = M.SCENARIOS["base"]
    d.rect(0, 0, W, H, fill=NAVY, r=0)
    d.c.setFillColor(TEAL)
    d.c.rect(60, H - 236, 7, 136, stroke=0, fill=1)
    d.text(88, 100, "PHYDRION", 44, XB, white)
    d.text(90, 156, "5억 원으로 MAU 30만, 그리고 미국 투자사의 후속 라운드", 20, B, TEAL)
    d.text(90, 188, "역노화 소비자를 입구로 한 노화 속도(Aging Velocity) AI 플랫폼", 12.5, R, SOFT)
    tiles = [("5억 원", "투자 요청 · 한국형 SAFE"), (f"{base.total_users / 10_000:,.0f}만", "12개월 누적 유저"),
             ("MAU 30만", "미국 투자사 후속 조건"), ("Cap 50억", "후속 전 마지막 진입가")]
    x = 60
    for v, l in tiles:
        d.kpi(x, 290, 200, 86, v, l, dark=True, accent=GOLD if v == "MAU 30만" else TEAL)
        x += 213.3
    d.text(60, 410, "제안안 · 대표 확정 전  |  모든 수치는 검증 전 목표·가설", 9, R, HexColor("#8aa0b8"))
    d.text(60, 480, "주식회사 피드리온 (Phydrion Inc.) · 대표 박상현 · thomas@phydrion.net · 2026-10", 8.5, R,
           HexColor("#8aa0b8"))


def product(d):
    d.new_page("PRODUCT & MOAT", "스마트폰 15초, 하드웨어 없이 노화 속도를 잽니다",
               note="현재 실적: 유료 판매 전(2026-09 기준 매출 0원) · 이번이 첫 외부 투자 라운드입니다. 세부 실적은 사업계획서 v3 Part 7.")
    d.para(44, 90, "'지금 수치'가 아니라 '변화의 속도와 가속도'를 봅니다. 건강검진이 1년에 한 번 찍는 사진이라면, Phydrion은 매일 돌아가는 CCTV입니다.",
           872, 11.5, R, INK)
    layers = [("1", "Dynamics Engine", "생체 신호 시계열 → 노화 속도·가속도"),
              ("2", "Reference Matching", "연령·성별 코호트 대비 위치"),
              ("3", "Correction Layer", "조도·움직임 보정 + 개인 기저선 학습"),
              ("4", "Latent Inference", "직접 측정 불가 지표를 신뢰 구간과 함께 추론")]
    d.text(44, 140, "PCP v3 — 4중 추론 엔진", 11, B, TEAL_D)
    t = 160
    for n, name, desc in layers:
        d.rect(44, t, 420, 50, fill=CARD, stroke=LINE)
        d.rect(54, t + 11, 28, 28, fill=NAVY, r=14)
        d.text(68, t + 18, n, 12, XB, white, anchor="c")
        d.text(96, t + 10, name, 11.5, XB, INK)
        d.text(96, t + 29, desc, 9.3, R, MUTED)
        t += 58
    d.text(496, 140, "이미 손에 쥔 것", 11, B, TEAL_D)
    assets = [("3건", "특허 출원 · 전부 심사청구", "노화 동역학 · 통합 플랫폼 P-01~P-05"),
              ("9건", "상표 등록·출원", "2027 Q2 PCT 출원 예정"),
              ("운영 중", "phydri.com · 달내영", "서비스 v8.16 (2026-09)"),
              ("0원", "측정 하드웨어 비용", "카메라 rPPG · 소프트웨어 엔진")]
    for i, (v, l, s) in enumerate(assets):
        x = 496 + (i % 2) * 214
        tt = 160 + (i // 2) * 112
        d.kpi(x, tt, 206, 100, v, l, s, accent=GOLD if i == 0 else TEAL)
    d.callout(44, 400, 872, 72,
              "측정(Measured)과 추론(Inferred)을 엄격히 구분하고 모든 추론값에 신뢰 구간을 붙입니다.\n"
              "웰니스로 시작해 SaMD(소프트웨어 의료기기)까지 확장할 수 있는 규제 설계이고, 후발주자가 복제하기 어려운 이유입니다.", 10.5)


def growth(d):
    d.new_page("GROWTH ENGINE · 5억 → 100만", "광고비 5억으로 100만 명을 모으는 산식",
               note="100만 = 12개월 누적 스캔 완료 유저(중복 제거). K = 유저 1명이 결과 카드 공유로 데려오는 신규 유저 수. 보수 시나리오: 40만 명.")
    base = M.SCENARIOS["base"]
    parts = [("유료 광고", base.paid_users, SERIES[0]), ("크리에이터", base.creator_users, SERIES[1]),
             ("Velocity Station", base.station_users, SERIES[2]), ("공공 시범사업", base.public_users, SERIES[3]),
             ("PR · 오가닉", base.organic_users, SERIES[4]), (f"바이럴 (K={base.k_factor})", base.viral_users, NAVY)]
    total = base.total_users
    top = 96
    x = 44
    for name, v, col in parts:
        w = 872 * v / total
        d.c.setFillColor(col)
        d.c.rect(x, H - top - 44, max(w - 2, 1), 44, stroke=0, fill=1)
        if w > 70:
            d.text(x + 8, top + 7, name, 8.5, B, white)
            d.text(x + 8, top + 22, f"{v / 10_000:.1f}만", 11, XB, white)
        x += w
    lx = 44
    for name, v, col in [parts[1], parts[3], parts[4]]:
        d.c.setFillColor(col)
        d.c.rect(lx, H - (top + 56) - 8, 8, 8, stroke=0, fill=1)
        d.text(lx + 12, top + 55, f"{name} {v / 10_000:.0f}만", 8.5, R, INK)
        lx += 130
    d.text(916, top + 54, f"시드 {base.seed_users / 10_000:.1f}만 ÷ (1 - K) = {total:,}명", 10.5, XB, INK, anchor="r")

    d.text(44, 186, "국가별 유료 집행 — 한국에서 증명하고 일본·미국으로", 11, B, TEAL_D)
    x = 44
    for m, when in zip(base.paid, ["M1~", "M5~", "M7~"]):
        d.rect(x, 206, 284, 92, fill=CARD, stroke=LINE)
        d.bar_top(x + 8, 206, 268, TEAL)
        d.text(x + 16, 220, f"{m.name}  ·  {when}", 12, XB, INK)
        d.text(x + 16, 244, M.eok(m.budget), 18, XB, INK)
        d.text(x + 100, 248, f"1명당 {m.cost_per_user:,}원 → {m.users / 10_000:.1f}만 명", 10, B, TEAL_D)
        d.text(x + 16, 274, {"한국": "H&B·약국 Station 결합, 공공 레퍼런스", "일본": "美肌·健康経営 수요, 현지화 후 단계 집행",
                             "미국": "롱제비티·생체나이 관심층, 크리에이터 중심"}[m.name], 9, R, MUTED)
        x += 294
    d.text(44, 318, "왜 이 단가가 가능한가", 11, B, TEAL_D)
    why = [("설치 없는 웹 스캔", "앱 설치 단계 이탈 제거"), ("결과 카드 = 광고", "'내 노화 속도'는 공유하고 싶은 형식"),
           ("성과형 크리에이터", "스캔 완료 건당 정산, 비용 상한 고정"), ("오프라인 Station", "매장 고객이 광고비 0원으로 유입")]
    x = 44
    for t, b in why:
        d.rect(x, 338, 211, 64, fill=white, stroke=LINE)
        d.text(x + 14, 350, t, 11, B, INK)
        d.text(x + 14, 372, b, 9, R, MUTED)
        x += 220
    d.callout(44, 418, 872, 56, "첫 60일은 3,000만 원만 씁니다(Gate 0). 1명당 비용 1,200원 이하 · K 0.3 이상이 실측되어야 본 예산이 열립니다.", 11)


def roadmap(d):
    d.new_page("12-MONTH PLAN", "MAU 30만까지 — 증명된 만큼만 다음 돈이 나갑니다", note=NOTE_TARGET)
    cum = M.monthly_cumulative(M.SCENARIOS["base"])
    cx, ctop, cw, ch = 74, 96, 430, 300
    base_y = H - ctop - ch
    vmax = 1_100_000
    c = d.c
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    for g in range(0, 110, 25):
        y = base_y + ch * g * 10_000 / vmax
        c.line(cx, y, cx + cw, y)
        d.text(cx - 6, H - y - 4, f"{g}만", 7.5, R, MUTED, anchor="r")
    step = cw / 12
    for series, col, ratio in ((cum, TEAL, 1.0), (cum, GOLD, M.MAU_RATIO)):
        pts = [(cx + step * (i + 0.5), base_y + ch * v * ratio / vmax) for i, v in enumerate(series)]
        c.setStrokeColor(col)
        c.setLineWidth(2)
        p = c.beginPath()
        p.moveTo(*pts[0])
        for pt in pts[1:]:
            p.lineTo(*pt)
        c.drawPath(p, stroke=1, fill=0)
        for i, (px, py) in enumerate(pts):
            c.setFillColor(white)
            c.circle(px, py, 4.5, stroke=0, fill=1)
            c.setFillColor(col)
            c.circle(px, py, 3.2, stroke=0, fill=1)
            if i in (2, 5, 8, 11) and col == TEAL:
                d.text(px, H - py - 20, f"{series[i] / 10_000:.0f}만", 10, XB, INK, anchor="c")
        d.text(cx + cw + 4, H - pts[-1][1] - 4, "누적" if col == TEAL else f"MAU {series[-1] * ratio / 10_000:.0f}만",
               9, B, col if col == GOLD else TEAL_D)
    for i in range(12):
        d.text(cx + step * (i + 0.5), ctop + ch + 8, f"M{i + 1}", 8, R, MUTED, anchor="c")
    d.text(560, 92, "집행 게이트", 11, B, TEAL_D)
    t = 112
    for name, when, spend, cond in M.GATES:
        last = name == "Gate 3"
        d.rect(560, t, 356, 66, fill=NAVY if last else CARD, stroke=None if last else LINE)
        d.text(574, t + 10, f"{name} · {when}", 11, XB, GOLD if last else TEAL_D)
        d.text(902, t + 11, spend, 9, B, SOFT if last else MUTED, anchor="r")
        d.para(574, t + 32, cond, 328, 10, B, white if last else INK)
        t += 74
    d.text(560, t + 6, "Q2 V-Lab 첫 수주 · Q3 일본 · Q4 미국 집행", 9.5, B, INK)


def revenue(d):
    d.new_page("BUSINESS MODEL", "앱은 입구 — 매출원은 다섯 개입니다", note=NOTE_TARGET)
    streams = M.revenue_streams()
    totals = M.revenue_totals()
    cx, ctop, cw, ch = 64, 100, 330, 320
    base_y = H - ctop - ch
    vmax = 120 * M.EOK
    c = d.c
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    for g in range(0, 121, 30):
        y = base_y + ch * g * M.EOK / vmax
        c.line(cx, y, cx + cw, y)
        d.text(cx - 6, H - y - 4, f"{g}억", 7.5, R, MUTED, anchor="r")
    for i, yl in enumerate(M.YEARS):
        bx = cx + 30 + i * 105
        acc = 0
        for s, col in zip(streams, SERIES):
            h = ch * s.values[i] / vmax
            c.setFillColor(col)
            c.rect(bx, base_y + acc, 64, max(h - 2, 0.5), stroke=0, fill=1)
            acc += h
        d.text(bx + 32, H - (base_y + acc) - 18, M.eok(totals[i]), 11, XB, INK, anchor="c")
        d.text(bx + 32, ctop + ch + 8, yl, 10, B, INK, anchor="c")
    desc = {
        "B2C 프리미엄": "노화 리포트 · 구독",
        "Velocity Station": "약국·H&B·피트니스 설치형 스캔 (월 5.9만)",
        "V-Lab 효능검증": "화장품·건기식 효능을 실사용 패널로 검증 (건당 3천만~1.5억)",
        "Velocity Commerce": "측정 결과 맞춤 제품 · 재측정이 재구매 트리거",
        "공단·지자체·보험": "V-SIB 성과공유 · 건강증진형 보험 · 기업 웰니스",
    }
    t = 96
    for s, col in zip(streams, SERIES):
        d.rect(430, t, 486, 62, fill=CARD, stroke=LINE)
        d.c.setFillColor(col)
        d.c.rect(430, H - t - 62, 6, 62, stroke=0, fill=1)
        d.text(448, t + 11, s.name, 11.5, XB, INK)
        d.text(448, t + 34, desc[s.name], 9, R, MUTED)
        d.text(902, t + 13, M.eok(s.values[2], 0), 16, XB, INK, anchor="r")
        d.text(902, t + 38, "2029 목표", 8, R, MUTED, anchor="r")
        t += 70
    d.text(430, t + 4, "핵심은 V-Lab: 광고비로 모은 유저가 B2B 매출로 회수되는 구조", 10, B, TEAL_D)


def nhis(d):
    nh = M.NhisModel()
    d.new_page("PUBLIC UPSIDE · NHIS", "건강보험공단이 '쓰지 않으면 안 나가는' 예방 예산",
               note="V-SIB 모델은 제안 단계이며 계약 확정 사항이 아닙니다. 가정: 위험군 10만 명, 연 발병률 3.5%, 조기개입 감소율 15%, 1인 연 진료비 70만 원.")
    d.para(44, 90, "보험료는 내지만 공단과 접점이 없는 '건강한 2050'을 역노화 동기로 데려옵니다. 공단은 측정·관리를 맡기고, "
                   "진료비 절감이 검증된 만큼만 성과보수로 지급합니다(V-SIB).", 872, 11.5)
    flow = [("역노화 유저", "매일 15초 스캔"), ("PHYDRION", "위험 Velocity 감지"), ("검진·보건소", "발병 전 조기 개입"),
            ("공단", "진료비 절감 → 30% 성과보수")]
    x = 44
    for i, (t1, t2) in enumerate(flow):
        dark = t1 == "PHYDRION"
        d.rect(x, 150, 196, 64, fill=NAVY if dark else CARD, stroke=None if dark else LINE)
        d.text(x + 98, 162, t1, 12.5, XB, white if dark else INK, anchor="c")
        d.text(x + 98, 186, t2, 9.5, R, HexColor("#9fd9e2") if dark else MUTED, anchor="c")
        if i < 3:
            d.arrow(x + 198, 182, x + 222, 182)
        x += 225
    d.kpi(44, 240, 205, 86, M.eok(nh.total_savings), "공단 5년 진료비 절감", f"연 {nh.avoided_per_year:,}명 발병 회피")
    d.kpi(261, 240, 205, 86, f"{nh.nhis_roi:.2f}배", "공단 ROI", f"순절감 {M.eok(nh.nhis_net)}", accent=SERIES[2])
    d.kpi(478, 240, 205, 86, M.eok(nh.phydrion_revenue), "Phydrion 5년 매출", "위험군 10만 명 1개 코호트", accent=GOLD)
    d.kpi(695, 240, 221, 86, "85%", "서류 처리비 절감", "특허 P-03 P2D 자동 디지털화", accent=SERIES[0])
    d.text(44, 348, "근거", 11, B, TEAL_D)
    facts = [("90조 원", "만성질환 진료비 (2024, 전체의 80.3%)"), ("4.5조 · 3.2조", "고혈압 · 2형 당뇨 진료비"),
             ("50개 지역", "건강생활실천지원금제 2026 시행 — 진입 경로")]
    x = 44
    for v, l in facts:
        d.rect(x, 368, 284, 54, fill=white, stroke=LINE)
        d.text(x + 14, 378, v, 15, XB, INK)
        d.text(x + 14, 402, l, 8.8, R, MUTED)
        x += 294
    d.callout(44, 436, 872, 42, "이 사업은 B2C가 커질수록 공공 계약의 협상력이 커지는, 후속 라운드의 '두 번째 성장 곡선'입니다.", 10.5)


def funds(d):
    d.new_page("USE OF FUNDS", "5억 원의 절반은 성장에, 나머지는 그 성장을 버티는 데",
               note="v3 대비 변경: 인건비 60% → 28%, 마케팅 12% → 50%. 임상 검증(n=100)은 후속 라운드에서 V-Lab·공공 시범사업과 묶어 확대합니다.")
    total = sum(b[2] for b in M.BUDGET_V4)
    t = 96
    for (name, desc, amt), col in zip(M.BUDGET_V4, [GOLD, TEAL, SERIES[0], SERIES[2], SERIES[4]]):
        d.text(44, t, name, 12, B, INK)
        d.text(480, t, f"{amt / total:.0%} · {M.eok(amt, 2)}", 12, XB, INK, anchor="r")
        d.text(44, t + 18, desc, 9.2, R, MUTED)
        d.rect(44, t + 36, 436, 9, fill=LINE, r=4)
        d.rect(44, t + 36, 436 * amt / total, 9, fill=col, r=4)
        t += 70
    d.rect(512, 96, 404, 340, fill=NAVY, r=10)
    d.text(532, 114, "투자자 보호 장치", 13, XB, white)
    prot = [("2회 분할 납입", "2.5억 즉시 + 2.5억 Gate 1(누적 10만) 통과 시"),
            ("게이트 집행", "Gate 0 미달이면 본 예산을 열지 않음"),
            ("월간 KPI 리포트", "유저 · 1명당 비용 · K · 재측정률 · MAU"),
            ("Pro-rata · MFN", "미국 투자사 후속 라운드 참여권, 최혜 조건")]
    tt = 146
    for k, v in prot:
        d.rect(532, tt, 364, 62, fill=NAVY2, r=8)
        d.text(548, tt + 11, k, 11.5, B, TEAL)
        d.para(548, tt + 33, v, 336, 9.5, R, white)
        tt += 70


def close(d):
    d.new_page("THE ASK", "첫 12개월을 함께 열어주십시오", dark=True)
    d.para(44, 92, "운영 중인 서비스, 심사청구된 특허 3건, 조건이 정해진 미국 투자사의 후속 라운드.\n"
                   "남은 것은 'MAU 30만'이라는 숫자 하나이고, 5억 원은 그 숫자를 만드는 데만 쓰입니다.", 872, 14, B, white, 23)
    d.text(44, 160, "투자자가 먼저 묻는 세 가지", 11, B, TEAL)
    qa = [("광고 단가가 더 비싸면?", "Gate 0에서 먼저 실측. 초과 시 성과형 크리에이터·Station으로 이동. 보수 시나리오도 누적 40만."),
          ("의료 광고 규제는?", "웰니스 포지셔닝: 진단·치료 표현 금지, 추정값에 신뢰 구간 명시. 광고 문구 사전 법무 검토."),
          ("1인 대표 리스크는?", "자금 28%로 AI 엔지니어·그로스 마케터 채용, 임상은 외부 자문. 후속 라운드에서 C-레벨 충원.")]
    x = 44
    for q, a in qa:
        d.rect(x, 180, 284, 118, fill=NAVY2, r=10)
        d.text(x + 16, 194, f"Q. {q}", 11, B, white)
        d.para(x + 16, 218, a, 252, 9.4, R, SOFT, 15)
        x += 294
    d.rect(44, 318, 872, 118, fill=NAVY2, r=10)
    d.text(64, 334, "투자 조건 (제안안 · 대표 확정 전)", 11, B, GOLD)
    d.para(64, 356, "· 5억 원 · 조건부지분인수계약(한국형 SAFE) · Post-money Cap 50억 원 · 2회 분할 납입\n"
                    "· 후속: 미국 소재 투자회사(사명은 실사 시 공개) · 조건 MAU 30만 · 30억 원 내외 협의 중\n"
                    "· 다음 단계: 실사 자료 공유(v3 · 특허 출원번호통지서 · 서비스 URL) → Gate 0 계획 합의 → 1차 납입",
           840, 10.5, R, white, 21)
    d.text(44, 458, "주식회사 피드리온 (Phydrion Inc.) · 대표 박상현 · thomas@phydrion.net · phydri.com · phydrion.io · phydrion.net",
           9, R, HexColor("#8aa0b8"))


PAGES = (cover, p_hook, product, growth, roadmap, revenue, nhis, funds, p_priming, close)


def build(path=OUT):
    register_fonts()
    d = Deck(path)
    for page in PAGES:
        page(d)
    d.save()
    return path


if __name__ == "__main__":
    print(build())
