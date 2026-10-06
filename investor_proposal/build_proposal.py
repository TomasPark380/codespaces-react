"""PHYDRION 마중물 투자 제안서(v4 보충) PDF 생성기.

사용법:
    pip install reportlab koreanize-matplotlib   # 폰트는 koreanize-matplotlib 의 나눔고딕 사용
    python build_proposal.py                      # → PHYDRION_Investment_Proposal_v4.pdf

폰트 경로를 직접 지정하려면 PHYDRION_FONT_DIR 환경변수에 NanumGothic*.ttf 가 있는 폴더를 넣는다.
"""

import importlib.util
import os
import sys

from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

import model as M

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "PHYDRION_Investment_Proposal_v4.pdf")
W, H = 960, 540

NAVY = HexColor("#0d1f3a")
NAVY2 = HexColor("#16304f")
TEAL = HexColor("#12a3b5")
TEAL_D = HexColor("#0b7d8c")
INK = HexColor("#0b1b2e")
MUTED = HexColor("#5b6b7c")
CARD = HexColor("#f2f6f9")
LINE = HexColor("#dde5ec")
GOLD = HexColor("#e0a526")
GOLD_BG = HexColor("#fff8e6")
SERIES = [HexColor(c) for c in ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4")]

R, B, XB = "NG", "NG-B", "NG-XB"


def register_fonts():
    candidates = [os.environ.get("PHYDRION_FONT_DIR", "")]
    spec = importlib.util.find_spec("koreanize_matplotlib")
    if spec and spec.origin:
        candidates.append(os.path.join(os.path.dirname(spec.origin), "fonts"))
    candidates.append(os.path.join(HERE, "fonts"))
    for d in candidates:
        if d and os.path.exists(os.path.join(d, "NanumGothic.ttf")):
            pdfmetrics.registerFont(TTFont(R, os.path.join(d, "NanumGothic.ttf")))
            pdfmetrics.registerFont(TTFont(B, os.path.join(d, "NanumGothicBold.ttf")))
            pdfmetrics.registerFont(TTFont(XB, os.path.join(d, "NanumGothicExtraBold.ttf")))
            return
    sys.exit("나눔고딕 폰트를 찾지 못했습니다: pip install koreanize-matplotlib 또는 PHYDRION_FONT_DIR 지정")


# ---------------------------------------------------------------------------
# 그리기 도구 — 좌표는 왼쪽 위 기준(top)으로 받아 내부에서 뒤집는다
# ---------------------------------------------------------------------------

class Deck:
    def __init__(self, path):
        self.c = canvas.Canvas(path, pagesize=(W, H))
        self.c.setTitle("PHYDRION 마중물 투자 제안서")
        self.c.setAuthor("주식회사 피드리온 (Phydrion Inc.)")
        self.page_no = 0

    # 기본 도형 ---------------------------------------------------------------
    def text(self, x, top, s, size=11, font=R, color=INK, anchor="l"):
        c = self.c
        c.setFont(font, size)
        c.setFillColor(color)
        y = H - top - size
        if anchor == "c":
            c.drawCentredString(x, y, s)
        elif anchor == "r":
            c.drawRightString(x, y, s)
        else:
            c.drawString(x, y, s)

    def para(self, x, top, s, width, size=10.5, font=R, color=INK, leading=None):
        """줄바꿈 문단. 다음 줄이 시작할 top 값을 돌려준다."""
        leading = leading or size * 1.45
        for raw in s.split("\n"):
            for line in simpleSplit(raw, font, size, width) or [""]:
                self.text(x, top, line, size, font, color)
                top += leading
        return top

    def rect(self, x, top, w, h, fill=CARD, stroke=None, r=8):
        c = self.c
        c.setFillColor(fill)
        if stroke:
            c.setStrokeColor(stroke)
            c.setLineWidth(0.8)
        c.roundRect(x, H - top - h, w, h, r, stroke=1 if stroke else 0, fill=1)

    def bar_top(self, x, top, w, color=TEAL, h=3):
        self.c.setFillColor(color)
        self.c.rect(x, H - top - h, w, h, stroke=0, fill=1)

    def arrow(self, x1, top1, x2, top2, color=TEAL_D, width=1.6):
        c = self.c
        y1, y2 = H - top1, H - top2
        c.setStrokeColor(color)
        c.setFillColor(color)
        c.setLineWidth(width)
        c.line(x1, y1, x2, y2)
        import math
        ang = math.atan2(y2 - y1, x2 - x1)
        L = 7
        p = c.beginPath()
        p.moveTo(x2, y2)
        p.lineTo(x2 - L * math.cos(ang - 0.4), y2 - L * math.sin(ang - 0.4))
        p.lineTo(x2 - L * math.cos(ang + 0.4), y2 - L * math.sin(ang + 0.4))
        p.close()
        c.drawPath(p, stroke=0, fill=1)

    def pill(self, x, top, s, fill=TEAL, color=white, size=8):
        w = pdfmetrics.stringWidth(s, B, size) + 12
        self.rect(x, top, w, size + 8, fill=fill, r=(size + 8) / 2)
        self.text(x + 6, top + 4, s, size, B, color)
        return w

    # 페이지 골격 -------------------------------------------------------------
    def new_page(self, kicker, title, dark=False, note=None):
        if self.page_no:
            self.c.showPage()
        self.page_no += 1
        self.rect(0, 0, W, H, fill=NAVY if dark else white, r=0)
        self.text(W - 44, 20, "PHYDRION · 마중물 투자 제안서 v4", 7.5, R,
                  HexColor("#8aa0b8") if dark else MUTED, anchor="r")
        self.text(44, 38, kicker, 8.5, B, TEAL)
        self.text(44, 54, title, 23, XB, white if dark else INK)
        foot = HexColor("#8aa0b8") if dark else MUTED
        if note:
            self.text(44, H - 26, note, 7.5, R, foot)
        self.text(W - 44, H - 26, f"{self.page_no:02d}", 7.5, R, foot, anchor="r")

    def card(self, x, top, w, h, title=None, body=None, accent=TEAL, size=9.5, fill=CARD):
        self.rect(x, top, w, h, fill=fill, stroke=LINE)
        self.bar_top(x + 8, top, w - 16, accent)
        t = top + 14
        if title:
            t = self.para(x + 14, t, title, w - 28, 11, B, INK, 15) + 4
        if body:
            t = self.para(x + 14, t, body, w - 28, size, R, INK if fill != NAVY2 else white)
        return t

    def kpi(self, x, top, w, h, value, label, sub=None, accent=TEAL, dark=False):
        self.rect(x, top, w, h, fill=NAVY2 if dark else CARD, stroke=None if dark else LINE)
        self.bar_top(x + 8, top, w - 16, accent)
        self.text(x + w / 2, top + 16, value, 21, XB, white if dark else INK, anchor="c")
        self.text(x + w / 2, top + 46, label, 9, B, TEAL if dark else TEAL_D, anchor="c")
        if sub:
            self.text(x + w / 2, top + 61, sub, 7.5, R, HexColor("#9fb3c8") if dark else MUTED, anchor="c")

    def table(self, x, top, widths, header, rows, size=9, row_h=22, bold_last_col=False, highlight=None):
        self.rect(x, top, sum(widths), row_h, fill=NAVY, r=3)
        cx = x
        for wcol, h in zip(widths, header):
            self.text(cx + 8, top + (row_h - size) / 2, h, size, B, white)
            cx += wcol
        t = top + row_h
        for i, row in enumerate(rows):
            if highlight is not None and i == highlight:
                self.rect(x, t, sum(widths), row_h, fill=GOLD_BG, r=0)
            elif i % 2:
                self.rect(x, t, sum(widths), row_h, fill=CARD, r=0)
            cx = x
            for j, (wcol, cell) in enumerate(zip(widths, row)):
                f = B if (j == 0 or (bold_last_col and j == len(row) - 1)) else R
                self.text(cx + 8, t + (row_h - size) / 2, str(cell), size, f, INK)
                cx += wcol
            t += row_h
        self.c.setStrokeColor(LINE)
        self.c.line(x, H - t, x + sum(widths), H - t)
        return t

    def callout(self, x, top, w, h, s, size=11, dark_bg=NAVY):
        self.rect(x, top, w, h, fill=dark_bg, r=8)
        self.para(x + 18, top + (h - size * 1.45 * (s.count("\n") + 1)) / 2 + 1, s, w - 36, size, B, white)

    def save(self):
        self.c.showPage()
        self.c.save()


# ---------------------------------------------------------------------------
# 페이지
# ---------------------------------------------------------------------------

NOTE_TARGET = "※ 모든 수치는 검증 전 목표·가설이며 model.py 의 가정으로 계산했습니다. 실적(2026-09 기준 매출 0원)은 v3 Part 7 참조."


def p_cover(d):
    d.page_no += 1
    d.rect(0, 0, W, H, fill=NAVY, r=0)
    d.c.setFillColor(TEAL)
    d.c.rect(60, H - 250, 7, 150, stroke=0, fill=1)
    d.text(88, 100, "PHYDRION", 44, XB, white)
    d.text(90, 158, "마중물 투자 제안서", 22, B, TEAL)
    d.text(90, 192, "5억 원이 여는 100만 유저 · 건강보험공단 성과공유 · 앱 밖의 매출", 13, R, HexColor("#c9d6e3"))
    d.rect(60, 300, 840, 120, fill=NAVY2, r=14)
    d.text(W / 2, 322, "미국 투자사의 후속 투자 조건은 MAU 30만. 필요한 것은 그 문을 여는 첫 12개월입니다.", 14, B, white, anchor="c")
    d.text(W / 2, 352, "역노화(안티에이징) 소비자를 미용 동기로 모으고, 그 데이터를 공단·지자체·기업이 사는 예방 의료 자산으로 바꿉니다.",
           10.5, R, HexColor("#c9d6e3"), anchor="c")
    d.text(W / 2, 378, "투자 요청 5억 원 · 조건부지분인수계약(한국형 SAFE) · Post-money Cap 50억 원 (제안안 · 대표 확정 전)",
           10, B, TEAL, anchor="c")
    d.text(60, 480, "주식회사 피드리온 (Phydrion Inc.) · 대표 박상현 · thomas@phydrion.net    |    "
           "2026-10 · 사업계획서 v3 보충 자료", 8.5, R, HexColor("#8aa0b8"))


def p_summary(d):
    d.new_page("EXECUTIVE SUMMARY", "세 가지 제안, 하나의 결론", note=NOTE_TARGET)
    base = M.SCENARIOS["base"]
    nh = M.NhisModel()
    totals = M.revenue_totals()
    cols = [
        ("제안 1 · 공단의 새 고객군", TEAL,
         f"공단 5년 순절감 {M.eok(nh.nhis_net)}",
         "보험료는 내지만 공단과 접점이 없는 '건강한 2050'을 역노화 동기로 끌어들입니다. "
         "검진 사이 363일을 Phydrion이 메우고, 공단은 검증된 절감액의 일부만 성과보수로 지급합니다 (V-SIB).\n"
         f"→ 위험군 10만 명 기준 공단 절감 {M.eok(nh.total_savings)}, ROI {nh.nhis_roi:.2f}배"),
        ("제안 2 · 앱 밖의 매출", SERIES[1],
         f"2029년 목표 매출 {M.eok(totals[2], 0)}",
         "앱은 입구일 뿐입니다. 오프라인 Velocity Station, 화장품·건기식 효능을 검증하는 V-Lab, "
         "측정 기반 커머스, 공공·보험 연동까지 매출원 5개를 하나의 엔진(PCP v3) 위에 얹습니다.\n"
         f"→ {M.YEARS[0]} {M.eok(totals[0])} → {M.YEARS[1]} {M.eok(totals[1], 0)} → {M.YEARS[2]} {M.eok(totals[2], 0)}"),
        ("제안 3 · 5억 → 100만 유저", GOLD,
         f"12개월 누적 {base.total_users / 10_000:,.0f}만 명",
         "설치 없는 웹 스캔 + 결과 카드 공유로 고객 획득 비용을 낮추고, 한국·일본·미국에 단계별로 집행합니다. "
         "60일 테스트(Gate 0)를 통과해야 본 예산을 씁니다.\n"
         f"→ 유료 {base.paid_users / 10_000:.1f}만 + 채널 {(base.seed_users - base.paid_users) / 10_000:.0f}만 "
         f"+ 바이럴 {base.viral_users / 10_000:.0f}만"),
    ]
    x = 44
    for title, accent, big, body in cols:
        d.rect(x, 96, 280, 222, fill=CARD, stroke=LINE)
        d.bar_top(x + 8, 96, 264, accent, 4)
        d.text(x + 16, 114, title, 11, B, TEAL_D)
        d.text(x + 16, 136, big, 17, XB, INK)
        d.para(x + 16, 176, body, 248, 11.2, R, INK, 19)
        x += 292
    deal = [("투자 요청", "5억 원"), ("방식", "한국형 SAFE"), ("Post-money Cap", "50억 원"),
            ("납입", "2회 분할"), ("운영 기간", "12개월"), ("후속 조건", "MAU 30만")]
    x = 44
    for k, v in deal:
        d.rect(x, 334, 140, 62, fill=white, stroke=LINE)
        d.text(x + 70, 346, k, 8.5, B, MUTED, anchor="c")
        d.text(x + 70, 364, v, 14, XB, INK, anchor="c")
        x += 146.4
    d.callout(44, 414, 872, 62,
              "5억 원은 운영비가 아니라 '후속 라운드 조건을 충족시키는 데 쓰는 돈'입니다. "
              "12개월 뒤 MAU 30만을 달성해 미국 투자사의 후속 투자를 엽니다.", 11.5)


def p_hook(d):
    d.new_page("WHY THIS WORKS", "미용 동기로 들어와, 건강 데이터로 남는다")
    d.para(44, 92, "사람들은 '혈압 관리'에는 지갑을 열지 않지만 '내 피부 나이'에는 매일 거울을 봅니다. "
                   "Phydrion은 역노화 욕구를 입구로 삼아, 스스로는 절대 건강관리 앱을 깔지 않을 사람들의 생체 신호를 매일 모읍니다.",
           872, 11.5, R, INK)
    steps = [
        ("입구", "역노화 · 뷰티", "피부 나이, 노화 속도 점수\n결과 카드 공유", SERIES[4]),
        ("습관", "매일 15초 스캔", "개인 기저선 형성\n변화 속도(Velocity) 추적", TEAL),
        ("전환", "건강 신호 감지", "HRV·피부 장벽 가속 시\n검진·보건소 연계 권유", SERIES[0]),
        ("가치", "예방 의료 자산", "공단·지자체·보험사·기업이\n사는 위험 감소 데이터", GOLD),
    ]
    x = 44
    for i, (k, t, b, col) in enumerate(steps):
        d.rect(x, 160, 196, 150, fill=CARD, stroke=LINE)
        d.bar_top(x + 8, 160, 180, col, 4)
        d.text(x + 16, 178, k, 9, B, TEAL_D)
        d.text(x + 16, 196, t, 15, XB, INK)
        d.para(x + 16, 230, b, 168, 10)
        if i < 3:
            d.arrow(x + 198, 235, x + 222, 235)
        x += 225
    d.kpi(44, 336, 280, 80, "90조 원", "비감염성(만성)질환 진료비", "2024 · 전체 진료비의 80.3% (질병관리청)")
    d.kpi(340, 336, 280, 80, "4.5조 · 3.2조", "고혈압 · 2형 당뇨 진료비", "단일 질환 기준 최상위 (2024)", accent=SERIES[0])
    d.kpi(636, 336, 280, 80, "연 12만 원", "건강생활실천지원금(예방형) 최대", "2026년 전국 50개 지역 시행", accent=GOLD)
    d.callout(44, 434, 872, 50, "역노화 시장은 '돈을 내고 스스로 측정하는' 고객군입니다. 공단이 가장 만나기 어려운 사람들을, 공단 예산 없이 데려옵니다.")


def p_nhis_model(d):
    d.new_page("PROPOSAL 1 · NHIS", "공단의 또 다른 고객군 — V-SIB 성과공유 모델",
               note="V-SIB: Velocity-linked Social Impact Bond. 공단·지자체 시범사업(건강생활실천지원금제 등) 참여를 출발점으로 제안합니다. 계약 확정 사항 아님.")
    # 다이어그램
    d.rect(44, 96, 520, 330, fill=CARD, stroke=LINE)
    nodes = {
        "user": (64, 140, "역노화 유저", "건강한 2050 · 위험 전 단계"),
        "phy": (234, 230, "PHYDRION", "PCP v3 · 매일 Velocity"),
        "nhis": (404, 140, "건강보험공단", "검진 · 지원금 · 빅데이터"),
        "care": (404, 330, "검진기관 · 보건소", "조기 개입 · 재측정"),
        "pay": (64, 330, "리워드 · 지원금", "건강생활실천 포인트"),
    }
    for key, (x, t, title, sub) in nodes.items():
        fill = NAVY if key == "phy" else white
        d.rect(x, t, 150, 58, fill=fill, stroke=None if key == "phy" else LINE)
        d.text(x + 75, t + 12, title, 11.5, XB, white if key == "phy" else INK, anchor="c")
        d.text(x + 75, t + 34, sub, 8, R, HexColor("#9fd9e2") if key == "phy" else MUTED, anchor="c")
    d.arrow(170, 198, 250, 230)
    d.text(150, 207, "매일 스캔", 8, B, TEAL_D)
    d.arrow(384, 230, 444, 198)
    d.text(400, 207, "익명 위험지표", 8, B, TEAL_D)
    d.arrow(479, 198, 479, 330)
    d.text(484, 258, "성과보수", 8, B, GOLD)
    d.arrow(384, 288, 420, 330)
    d.text(330, 312, "위험 가속 시 연계", 8, B, TEAL_D)
    d.arrow(234, 288, 200, 330)
    d.text(130, 300, "실천 인증", 8, B, TEAL_D)
    d.arrow(139, 330, 139, 198, color=GOLD)
    d.text(84, 258, "동기 강화", 8, B, GOLD)
    d.text(64, 404, "공단은 '측정·관리'를 외주하고, 절감이 검증된 만큼만 지급합니다.", 9, B, INK)

    x = 580
    t = 96
    blocks = [
        ("① 기본 운영수수료", f"참여자 1인·연 {M.NhisModel().base_fee:,}원 — 측정·리포트·위험군 선별", TEAL),
        ("② 성과보수 (Gain-share)", "검증된 진료비 절감액의 30% — 효과 없으면 지급 없음", GOLD),
        ("③ 처리비용 절감 (P2D)", "검진 결과지·진료 서류 자동 디지털화(특허 P-03)로 서류 처리비 85% 절감", SERIES[0]),
    ]
    for title, body, col in blocks:
        d.rect(x, t, 336, 72, fill=CARD, stroke=LINE)
        d.bar_top(x + 8, t, 320, col)
        d.text(x + 14, t + 14, title, 11, B, INK)
        d.para(x + 14, t + 34, body, 308, 9.3)
        t += 82
    d.callout(x, t + 4, 336, 80,
              "공단이 얻는 것:\n① 접점 없던 납부자 ② 검진 사이 363일 데이터\n③ 쓰지 않으면 돈이 안 나가는 예방 예산", 10)


def p_nhis_numbers(d):
    nh = M.NhisModel()
    p2d = M.P2DModel()
    d.new_page("PROPOSAL 1 · SIMULATION", "위험군 10만 명이면 공단은 5년간 얼마를 아끼는가",
               note="가정: 연 발병률 3.5%, 조기개입 감소율 15%(원본 인용 WHO 20~30%보다 보수적), 1인 연 진료비 70만 원, 합병증 절감 미반영. 실증 연구로 확정 예정.")
    d.kpi(44, 92, 205, 82, f"{nh.avoided_per_year:,}명/년", "회피 발병자", f"10만 × {nh.onset_rate:.1%} × {nh.reduction:.0%}")
    d.kpi(261, 92, 205, 82, M.eok(nh.total_savings), "공단 5년 진료비 절감", "회피자는 해마다 누적", accent=SERIES[0])
    d.kpi(478, 92, 205, 82, M.eok(nh.phydrion_revenue), "Phydrion 5년 매출", f"운영 {M.eok(nh.phydrion_fee)} + 성과 {M.eok(nh.phydrion_share)}", accent=GOLD)
    d.kpi(695, 92, 221, 82, f"{nh.nhis_roi:.2f}배", "공단 ROI", f"순절감 {M.eok(nh.nhis_net)}", accent=SERIES[2])

    rows = []
    for i, s in enumerate(nh.yearly_savings(), start=1):
        share = s * nh.gain_share
        fee = nh.cohort * nh.base_fee
        rows.append((f"{i}년차", f"{nh.avoided_per_year * i:,}명", M.eok(s), M.eok(fee + share), M.eok(s - fee - share)))
    rows.append(("합계", "", M.eok(nh.total_savings), M.eok(nh.phydrion_revenue), M.eok(nh.nhis_net)))
    d.text(44, 196, "연차별 절감 흐름 (위험군 10만 명 코호트)", 11, B, TEAL_D)
    d.table(44, 216, [80, 110, 110, 120, 120], ["연차", "누적 회피자", "공단 절감", "Phydrion 수령", "공단 순절감"],
            rows, highlight=len(rows) - 1)

    d.rect(600, 196, 316, 230, fill=CARD, stroke=LINE)
    d.bar_top(608, 196, 300, SERIES[0])
    d.text(616, 212, "병원비 '처리' 비용도 줄입니다 — P2D", 11, B, INK)
    d.para(616, 236, "검진 결과지·진료 서류를 사람이 옮겨 적는 비용을 특허 P-03(기관별 Template DB 기반 P2D 자동 디지털화)으로 대체합니다. "
                     "검진기관·보험사의 실손 청구 서류 처리에도 그대로 씁니다.", 284, 9.3)
    d.table(616, 318, [150, 134], ["항목 (연 500만 건 가정)", "값"], [
        ("건당 수기 처리비", f"{p2d.manual_cost:,}원"),
        ("건당 자동 처리비", f"{p2d.auto_cost:,}원"),
        ("연간 처리비 절감", M.eok(p2d.saving)),
        ("Phydrion 수수료(건당 200원)", M.eok(p2d.revenue)),
    ], size=8.5, row_h=20, bold_last_col=True)


def p_revenue_axes(d):
    d.new_page("PROPOSAL 2 · BEYOND THE APP", "앱만으로는 안 됩니다 — 매출의 다른 네 축",
               note="Velocity Station은 기존 피부관리샵 화이트라벨 태블릿(설치 49만 + 월 4.9만)을 약국·H&B 매장·피트니스·검진센터로 넓힌 형태입니다.")
    axes = [
        ("Velocity Station", "오프라인 스캔 스테이션", SERIES[0],
         "태블릿 + 표준 조명 키트를 약국·H&B 매장·피트니스·검진센터에 설치. 매장은 고객에게 '오늘의 노화 속도'를 보여주고 상담·판매로 연결.",
         "월 5.9만 원 구독 + 스캔당 과금 + 매장 내 광고", "매장이 유저를 데려오는 B2B2C 유입 채널"),
        ("V-Lab", "분산형 효능검증 플랫폼", SERIES[2],
         "화장품·건기식 회사가 신제품 효과를 수천 명의 실사용 피부·생체 변화로 검증. 4주 사용 전후 Velocity 비교 리포트 제공 (동의 기반).",
         "프로젝트당 3,000만~1.5억 원", "100만 유저 = 국내 최대 실사용 노화 패널"),
        ("Velocity Commerce", "측정 기반 맞춤 처방", SERIES[1],
         "피부 장벽·색소·HRV 가속 신호에 맞춘 제품·루틴 큐레이션. '측정 → 사용 → 재측정'으로 효과가 보이는 커머스.",
         "제휴 수수료 15% → 이후 PB 상품", "재측정이 곧 재구매 트리거"),
        ("B2E · 보험", "기업 임직원 · 건강증진형 보험", SERIES[4],
         "기업 복지 웰니스 패키지와 보험사 건강증진형 상품에 노화 속도 지표를 공급. 위험 등급 API로 B2B 라이선스와 연결.",
         "1인당 월 2,000~5,000원", "v3의 B2B AI 라이선스와 같은 엔진"),
    ]
    x = 44
    for name, sub, col, body, price, why in axes:
        d.rect(x, 92, 211, 360, fill=CARD, stroke=LINE)
        d.bar_top(x + 8, 92, 195, col, 4)
        d.text(x + 14, 110, name, 14, XB, INK)
        d.text(x + 14, 132, sub, 9, B, TEAL_D)
        t = d.para(x + 14, 158, body, 183, 10.8, R, INK, 17)
        d.rect(x + 10, 330, 191, 52, fill=white, stroke=LINE, r=6)
        d.text(x + 18, 338, "과금", 8, B, MUTED)
        d.para(x + 18, 352, price, 175, 9, B, INK)
        d.text(x + 14, 392, "왜 강한가", 8, B, MUTED)
        d.para(x + 14, 406, why, 183, 9, R, INK)
        x += 219
    d.callout(44, 462, 872, 38, "하드웨어는 '가볍게', 데이터는 '깊게' — 모든 축이 같은 PCP v3 엔진과 같은 유저 기저선을 공유합니다.", 10.5)


def p_vlab(d):
    d.new_page("PROPOSAL 2 · BREAKTHROUGH", "V-Lab — 유저가 많아질수록 B2B 매출이 커지는 구조",
               note="V-Lab은 웰니스 범위의 실사용 데이터 리포트이며, 법정 인체적용시험·임상시험을 대체한다고 표방하지 않습니다(보완 자료로 제공).")
    d.para(44, 92, "화장품·건기식 회사는 신제품마다 효능 근거를 사야 합니다. 기존 방식은 소수 피험자를 기관에 불러 수주간 측정하는 방식이라 비싸고 느립니다. "
                   "V-Lab은 이미 매일 스캔하는 유저 중 조건에 맞는 사람을 모집해, 집에서 4주간 사용 전후 변화를 측정합니다.", 872, 10.5)
    d.table(44, 160, [200, 236, 236], ["비교", "기존 기관 방문형 측정", "V-Lab (분산형 · 스마트폰)"], [
        ("피험자 규모", "수십 명", "수백~수천 명"),
        ("모집·측정 기간", "수주~수개월", "모집 72시간 · 측정 4주"),
        ("측정 빈도", "방문 시 2~3회", "매일 (연속 Velocity 곡선)"),
        ("결과물", "전후 비교 수치", "전후 + 반응군 세분화 + 실사용 맥락"),
        ("Phydrion 과금", "-", "프로젝트당 3,000만~1.5억 원"),
    ], size=9.5, row_h=26)
    flywheel = ["유저 증가", "패널 다양성↑", "V-Lab 수주↑", "유저 리워드·무료 제품", "재측정·잔존↑"]
    d.text(740, 160, "플라이휠", 11, B, TEAL_D)
    t = 182
    for i, s in enumerate(flywheel):
        d.rect(740, t, 176, 30, fill=NAVY if i == 2 else CARD, stroke=None if i == 2 else LINE, r=6)
        d.text(828, t + 9, s, 10, B, white if i == 2 else INK, anchor="c")
        if i < len(flywheel) - 1:
            d.arrow(828, t + 30, 828, t + 40)
        t += 40
    d.callout(44, 330, 672, 70, "유저는 무료 제품과 리워드를 받고, 브랜드는 빠른 근거를 얻고, Phydrion은 데이터가 쌓일수록\n"
                               "단가와 수주가 함께 오릅니다. 광고비로 모은 유저가 B2B 매출로 회수되는 구조입니다.", 10.5)
    vl = M.revenue_streams()[2]
    for i, (y, v) in enumerate(zip(M.YEARS, vl.values)):
        d.kpi(44 + i * 228, 414, 216, 76, M.eok(v), f"V-Lab {y} 목표", f"프로젝트 {[4, 15, 35][i]}건 × 평균 6,000만 원", accent=SERIES[2])


def p_revenue_chart(d):
    d.new_page("PROPOSAL 2 · REVENUE MIX", "3개년 매출 목표 — 다섯 개의 매출원", note=NOTE_TARGET)
    streams = M.revenue_streams()
    totals = M.revenue_totals()
    # 누적 막대 그래프
    cx, ctop, cw, ch = 64, 100, 420, 330
    base_y = H - ctop - ch
    vmax = 120 * M.EOK
    c = d.c
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    for g in range(0, 121, 30):
        y = base_y + ch * g * M.EOK / vmax
        c.line(cx, y, cx + cw, y)
        d.text(cx - 6, H - y - 4, f"{g}억", 7.5, R, MUTED, anchor="r")
    bw = 70
    for i, y_label in enumerate(M.YEARS):
        bx = cx + 50 + i * 135
        acc = 0
        for s, col in zip(streams, SERIES):
            v = s.values[i]
            h = ch * v / vmax
            c.setFillColor(col)
            c.rect(bx, base_y + acc, bw, max(h - 2, 0.5), stroke=0, fill=1)   # 2px 간격
            acc += h
        d.text(bx + bw / 2, H - (base_y + acc) - 18, M.eok(totals[i]), 11, XB, INK, anchor="c")
        d.text(bx + bw / 2, ctop + ch + 8, y_label, 10, B, INK, anchor="c")
    # 범례 + 표
    d.text(520, 100, "매출원별 목표 (단위: 억 원)", 11, B, TEAL_D)
    rows = []
    for s in streams:
        rows.append(["     " + s.name] + [f"{v / M.EOK:,.1f}" for v in s.values])
    rows.append(["합계"] + [f"{v / M.EOK:,.1f}" for v in totals])
    t = d.table(520, 120, [150, 75, 75, 96], ["매출원"] + M.YEARS, rows, size=9, row_h=24, highlight=len(rows) - 1)
    for i, col in enumerate(SERIES):
        c.setFillColor(col)
        c.roundRect(528, H - (120 + 24 * (i + 1)) - 16, 6, 8, 1.5, stroke=0, fill=1)
    d.text(520, t + 12, "산식", 9, B, MUTED)
    tt = t + 28
    for s in streams:
        tt = d.para(520, tt, f"· {s.name}: {s.note}", 396, 8.3, R, MUTED, 12)


def p_users_funnel(d):
    d.new_page("PROPOSAL 3 · 1,000,000 USERS", "5억 원으로 100만 유저 — 퍼널 산식",
               note="100만 = 12개월 누적 스캔 완료 유저(1회 이상 측정, 중복 제거). MAU 목표는 누적의 30%(후속 투자 조건 MAU 30만). K = 유저 1명이 결과 카드 공유로 데려오는 신규 스캔 유저 수.")
    base = M.SCENARIOS["base"]
    parts = [
        ("유료 광고", base.paid_users, SERIES[0]),
        ("크리에이터", base.creator_users, SERIES[1]),
        ("Velocity Station", base.station_users, SERIES[2]),
        ("공공 시범사업", base.public_users, SERIES[3]),
        ("PR · 오가닉", base.organic_users, SERIES[4]),
    ]
    d.text(44, 92, "기본 시나리오 유입 구성", 11, B, TEAL_D)
    total = base.total_users
    x0, top, wbar = 44, 114, 872
    x = x0
    for name, v, col in parts + [("바이럴 (K=0.6)", base.viral_users, NAVY)]:
        w = wbar * v / total
        d.c.setFillColor(col)
        d.c.rect(x, H - top - 34, max(w - 2, 1), 34, stroke=0, fill=1)
        if w > 60:
            d.text(x + 6, top + 4, name, 8, B, white)
            d.text(x + 6, top + 18, f"{v / 10_000:.1f}만", 9, XB, white)
        x += w
    d.text(916, top + 42, f"합계 {total:,}명", 10, XB, INK, anchor="r")
    lx = 300
    for name, v, col in parts[1:2] + parts[3:]:
        d.c.setFillColor(col)
        d.c.rect(lx, H - (top + 44) - 8, 8, 8, stroke=0, fill=1)
        d.text(lx + 12, top + 43, f"{name} {v / 10_000:.0f}만", 8.5, R, INK)
        lx += 120
    d.text(44, top + 42, f"시드 {base.seed_users:,}명 ÷ (1 - K {base.k_factor}) = {total:,}명", 9.5, B, MUTED)

    rows = []
    for s in M.SCENARIOS.values():
        rows.append((s.label, f"{s.paid_users:,}", f"{s.seed_users - s.paid_users:,}", f"{s.k_factor}",
                     f"{s.viral_users:,}", f"{s.total_users:,}", f"{int(s.total_users * M.MAU_RATIO):,}"))
    d.text(44, 196, "시나리오", 11, B, TEAL_D)
    d.table(44, 216, [70, 100, 100, 60, 100, 110, 100], ["시나리오", "유료 광고", "채널 유입", "K", "바이럴", "누적 유저", "MAU"],
            rows, highlight=1, bold_last_col=True)
    d.rect(700, 196, 216, 112, fill=GOLD_BG, stroke=GOLD)
    d.text(712, 208, "MAU 30만을 지키는 장치", 11, XB, INK)
    d.para(712, 228, "14일 재측정 알림·리워드, Station 재방문 스캔, 건강생활실천 포인트 연동으로 MAU 30%를 유지합니다. "
                     "보수 시나리오(MAU 12만)면 M6에 광고를 리텐션 예산으로 돌립니다.", 192, 8.6, R, INK, 12.5)

    d.text(44, 330, "왜 이 단가가 가능한가", 11, B, TEAL_D)
    why = [
        ("설치 없는 웹 스캔", "phydri.com에서 바로 15초 측정 → 앱 설치 단계 이탈 제거"),
        ("결과 카드가 광고", "'내 노화 속도' 카드는 공유 욕구가 높은 형식 → 바이럴 계수 확보"),
        ("성과형 크리에이터", "선지급 대신 스캔 완료 건당 정산 → 비용 상한 고정"),
        ("오프라인이 데려오는 유저", "Station 매장 고객이 무료로 첫 스캔 → 광고비 0원 유입"),
    ]
    x = 44
    for t, b in why:
        d.card(x, 350, 211, 100, t, b, size=9.2)
        x += 220


def p_markets(d):
    d.new_page("PROPOSAL 3 · KR · JP · US", "국가별 집행 — 한국에서 증명하고 일본·미국으로", note=NOTE_TARGET)
    base = M.SCENARIOS["base"]
    msgs = {
        "한국": ("피부 나이 · 뷰티 테크", "올리브영형 H&B·약국 Station과 결합, 공단·지자체 시범사업 레퍼런스 확보"),
        "일본": ("美肌 · 健康経営", "피부 미용 관심도와 기업 건강경영 수요 — 일본어 UX·현지 결제부터 소규모 시작"),
        "미국": ("Longevity · Biological Age", "생체나이·롱제비티 관심층 대상 영어 웹 스캔, 크리에이터 중심 집행"),
    }
    x = 44
    for m in base.paid:
        head, body = msgs[m.name]
        d.rect(x, 92, 284, 250, fill=CARD, stroke=LINE)
        d.bar_top(x + 8, 92, 268, TEAL, 4)
        d.text(x + 16, 110, m.name, 18, XB, INK)
        d.text(x + 16, 138, head, 10, B, TEAL_D)
        d.text(x + 16, 168, M.eok(m.budget), 22, XB, INK)
        d.text(x + 16, 198, "유료 광고 예산", 8.5, R, MUTED)
        d.text(150 + x, 168, f"{m.cost_per_user:,}원", 22, XB, INK)
        d.text(150 + x, 198, "스캔 1명당 비용(목표)", 8.5, R, MUTED)
        d.text(x + 16, 224, f"유료 유입 {m.users:,}명", 12, B, INK)
        d.para(x + 16, 250, body, 252, 9.3)
        x += 294
    d.text(44, 362, "집행 순서", 11, B, TEAL_D)
    seq = [("M1–M2", "한국 Gate 0 테스트", "3,000만 원으로 단가·K 실측"),
           ("M3–M5", "한국 본 집행", "Station 100곳 · 크리에이터 확장"),
           ("M5–M8", "일본 진입", "현지화 완료 후 단계 집행"),
           ("M7–M12", "미국 진입", "롱제비티 크리에이터 중심")]
    x = 44
    for i, (when, what, how) in enumerate(seq):
        d.rect(x, 382, 208, 70, fill=NAVY, r=8)
        d.text(x + 14, 394, when, 10, XB, TEAL)
        d.text(x + 14, 412, what, 11, B, white)
        d.text(x + 14, 432, how, 8.8, R, HexColor("#c9d6e3"))
        if i < 3:
            d.arrow(x + 210, 417, x + 220, 417)
        x += 222


def p_budget(d):
    d.new_page("PROPOSAL 3 · USE OF FUNDS", "5억 원 사용처 재설계 — 인건비 중심에서 성장 중심으로",
               note="v3(제안안): 인건비 60% · 임상 15% · 영업·마케팅 12% · 인프라 8% · IP 5%. 임상 검증(n=100)은 V-Lab·공공 시범사업과 묶어 후속 라운드에서 확대 집행합니다.")
    total = sum(b[2] for b in M.BUDGET_V4)
    t = 96
    for (name, desc, amt), col in zip(M.BUDGET_V4, [GOLD, TEAL, SERIES[0], SERIES[2], SERIES[4]]):
        d.text(44, t, name, 11, B, INK)
        d.text(470, t, f"{amt / total:.0%} · {M.eok(amt, 2)}", 11, XB, INK, anchor="r")
        d.text(44, t + 16, desc, 8.8, R, MUTED)
        d.rect(44, t + 32, 426, 8, fill=LINE, r=4)
        d.rect(44, t + 32, 426 * amt / total, 8, fill=col, r=4)
        t += 62
    d.text(500, 92, "집행 게이트 — 조건을 넘어야 다음 돈이 나갑니다", 11, B, TEAL_D)
    d.table(500, 112, [62, 46, 104, 204], ["게이트", "시점", "누적 집행", "통과 조건"],
            [g for g in M.GATES], size=8.6, row_h=30)
    d.callout(500, 264, 416, 120,
              "투자자 보호 장치 (제안)\n· 2회 분할 납입: 2.5억(즉시) + 2.5억(Gate 1 통과 시)\n"
              "· 월간 KPI 리포트(유저·단가·K·재측정률) 공유\n· 후속 라운드 Pro-rata 참여권 · MFN 조항", 10)
    d.text(500, 404, f"운영 기간 12개월 = 후속 라운드 시점과 일치 (v3: 18개월)", 9.5, B, INK)


def p_roadmap(d):
    d.new_page("PROPOSAL 3 · 12-MONTH ROADMAP", "월별 누적 유저 목표", note=NOTE_TARGET)
    cum = M.monthly_cumulative(M.SCENARIOS["base"])
    bear = M.monthly_cumulative(M.SCENARIOS["bear"])
    cx, ctop, cw, ch = 74, 96, 560, 300
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
    for series, col in ((bear, MUTED), (cum, TEAL)):
        c.setStrokeColor(col)
        c.setLineWidth(2)
        pts = [(cx + step * (i + 0.5), base_y + ch * v / vmax) for i, v in enumerate(series)]
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
            if col == TEAL and i in (2, 5, 8, 11):
                d.text(px, H - py - 20, f"{series[i] / 10_000:.0f}만", 10, XB, INK, anchor="c")
    for i in range(12):
        d.text(cx + step * (i + 0.5), ctop + ch + 8, f"M{i + 1}", 8, R, MUTED, anchor="c")
    d.text(cx + cw, H - (base_y + ch * bear[-1] / vmax) + 6, f"보수 {bear[-1] / 10_000:.0f}만", 8.5, B, MUTED, anchor="r")
    d.rect(660, 96, 256, 300, fill=CARD, stroke=LINE)
    d.text(676, 110, "분기별 마일스톤", 11, B, TEAL_D)
    ms = [("Q1", "한국 Gate 0 통과 · Station 30곳 · 누적 8만"),
          ("Q2", "누적 34만 · V-Lab 첫 수주 · 공공 시범 제안"),
          ("Q3", "일본 집행 · 누적 68만 · 커머스 오픈"),
          ("Q4", "미국 집행 · 누적 100만 · MAU 30만 → 미국 투자사 후속 라운드")]
    t = 136
    for q, s in ms:
        d.text(676, t, q, 12, XB, TEAL)
        t = d.para(710, t, s, 190, 9.5) + 12


def p_priming(d):
    d.new_page("THE ASK · PRIMING CAPITAL", "왜 '마중물'인가 — 후속 투자는 정해져 있습니다", dark=True,
               note="후속 투자사명은 비밀유지 약정에 따라 실사 단계에서 공개합니다. 지분가치는 예시 계산이며 수익을 보장하지 않습니다(SAFE Post-money Cap 50억, 후속 30억 조달 가정).")
    d.rect(44, 92, 420, 170, fill=NAVY2, r=10)
    d.text(62, 108, "후속 라운드 — 미국 투자사", 11, B, TEAL)
    d.para(62, 132, "투자 기관: 미국 소재 투자회사 (사명은 실사 시 공개)\n투자 조건: MAU 30만 달성\n"
                    "예상 규모: 30억 원 내외 (협의 중)", 384, 10.5, R, white, 18)
    d.para(62, 202, "후속 투자자는 '숫자'를 기다리고 있습니다. 마중물 5억은 그 숫자를 12개월 안에 만드는 돈입니다.", 384, 10, B, GOLD)
    d.rect(480, 92, 436, 170, fill=NAVY2, r=10)
    d.text(498, 108, "마중물 투자자가 얻는 것", 11, B, TEAL)
    d.para(498, 132, "① 가장 낮은 가격: 후속 라운드 전 유일한 진입 시점 (Cap 50억)\n"
                     "② 리스크 축소: 출구 조건(후속 투자자)이 이미 존재\n"
                     "③ 분할 납입 + 게이트: 증명된 만큼만 집행\n"
                     "④ 후속 라운드 Pro-rata 참여권", 400, 10, R, white, 19)
    d.text(44, 282, "후속 라운드 기업가치별 마중물 지분 가치 (예시)", 11, B, TEAL)
    rows = [(M.eok(pre, 0), M.eok(post, 0), f"{dil:.1%}", M.eok(val, 0), f"{mult:.1f}배")
            for pre, post, dil, val, mult in M.step_up_table()]
    t = 302
    widths = [170, 170, 170, 180, 182]
    hdr = ["후속 Pre-money", "후속 Post-money", "희석 후 지분", "지분 가치", "투자금 대비"]
    d.rect(44, t, sum(widths), 24, fill=TEAL_D, r=3)
    x = 44
    for wcol, h in zip(widths, hdr):
        d.text(x + 10, t + 7, h, 9.5, B, white)
        x += wcol
    t += 24
    for i, row in enumerate(rows):
        d.rect(44, t, sum(widths), 28, fill=NAVY2 if i % 2 == 0 else NAVY, r=0)
        x = 44
        for j, (wcol, cell) in enumerate(zip(widths, row)):
            d.text(x + 10, t + 8, cell, 11 if j >= 3 else 10, XB if j >= 3 else R, GOLD if j == 4 else white)
            x += wcol
        t += 28
    d.para(44, t + 14, "5억 원 × 10% (Post-money Cap 50억) → 후속 30억 조달로 희석되어도, 후속 기업가치 150억이면 3배, 250억이면 5배의 장부가치.",
           872, 10, B, white)


def p_risks(d):
    d.new_page("RISKS & ANSWERS", "투자자가 물을 질문에 먼저 답합니다")
    qa = [
        ("광고 단가가 목표보다 비싸면?", "Gate 0(3,000만 원)에서 먼저 실측합니다. 1명당 1,200원 초과 시 유료 비중을 줄이고 Station·크리에이터(성과형)로 이동합니다. 보수 시나리오에서도 40만 명."),
        ("의료 광고·규제 문제는?", "웰니스 포지셔닝 유지: '진단·치료' 표현 금지, 추정값에는 신뢰 구간과 '임상 대체 불가'를 명시(v3 투명성 원칙). 광고 문구는 사전 법무 검토 예산 반영."),
        ("공단이 정말 계약하나?", "확정 아님. 건강생활실천지원금제·보건소 모바일 헬스케어 등 기존 시범사업 참여부터 시작하고, 성과보수형이라 공단 입장에서 손실 위험이 작은 구조로 제안합니다."),
        ("100만 유저 서버비는?", "rPPG·영상 분석 상당 부분을 기기 내(온디바이스)에서 처리하고 요약값만 전송해 유저당 서버비를 낮춥니다. 인프라·보안 3,500만 원 반영."),
        ("일본·미국 개인정보는?", "국가별 동의·국외이전 고지, 일본 APPI·미국 FTC 건강정보 규정 검토. 현지화 예산(4,000만 원)에 포함. 민감 원본 영상은 저장하지 않는 것이 원칙."),
        ("1인 대표 리스크는?", "자금 28%로 AI 엔지니어·그로스 마케터 채용, 임상 책임자는 외부 자문 계약으로 보완(v3 Part 6). 후속 라운드에서 C-레벨 충원."),
    ]
    x0, t0 = 44, 92
    for i, (q, a) in enumerate(qa):
        x = x0 + (i % 2) * 442
        t = t0 + (i // 2) * 128
        d.rect(x, t, 430, 116, fill=CARD, stroke=LINE)
        d.bar_top(x + 8, t, 414, TEAL if i % 2 == 0 else SERIES[0])
        d.text(x + 16, t + 14, f"Q. {q}", 11, B, INK)
        d.para(x + 16, t + 40, a, 398, 10.5, R, INK, 17)


def p_close(d):
    d.new_page("CLOSING", "첫 12개월을 함께 열어주십시오", dark=True)
    d.para(44, 100, "운영 중인 서비스, 출원·심사청구된 특허 3건, 그리고 이미 정해진 후속 라운드.\n"
                    "남은 것은 미국 투자사가 제시한 'MAU 30만'이라는 숫자 하나입니다.", 700, 15, B, white, 24)
    items = [("5억 원", "투자 요청 · 한국형 SAFE"), ("MAU 30만", "후속 투자 조건 · 누적 100만"),
             ("5개", "앱 밖 매출원 포함 매출 축"), ("1.75배", "공단 ROI (위험군 10만 기준)")]
    x = 44
    for v, l in items:
        d.kpi(x, 200, 208, 86, v, l, dark=True)
        x += 221
    d.rect(44, 316, 872, 110, fill=NAVY2, r=10)
    d.text(64, 332, "다음 단계 (제안)", 11, B, TEAL)
    d.para(64, 354, "① 투자 의향 확인 및 실사 자료(v3 사업계획서 · 특허 출원번호통지서 · 서비스 URL) 공유\n"
                    "② Gate 0 테스트 계획서 및 KPI 리포트 양식 합의\n"
                    "③ SAFE 조건(Cap · 분할 납입 · Pro-rata) 확정 및 1차 납입", 840, 10.5, R, white, 20)
    d.text(44, 456, "주식회사 피드리온 (Phydrion Inc.) · 대표 박상현 · thomas@phydrion.net · phydri.com · phydrion.io · phydrion.net",
           9, R, HexColor("#8aa0b8"))


def build(path=OUT):
    register_fonts()
    d = Deck(path)
    for page in (p_cover, p_summary, p_hook, p_nhis_model, p_nhis_numbers, p_revenue_axes, p_vlab,
                 p_revenue_chart, p_users_funnel, p_markets, p_budget, p_roadmap, p_priming, p_risks, p_close):
        page(d)
    d.save()
    return path


if __name__ == "__main__":
    print(build())
