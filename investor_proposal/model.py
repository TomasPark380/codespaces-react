"""PHYDRION 마중물 투자 제안서 — 수치 모델.

제안서(build_proposal.py)에 들어가는 모든 숫자는 이 파일에서 계산한다.
가정을 바꾸면 PDF를 다시 빌드하는 것만으로 전 페이지 수치가 함께 바뀐다.
모든 값은 검증 전 목표·가설이며, 실측치가 아니다.
"""

from dataclasses import dataclass, field

EOK = 100_000_000  # 1억 원
MAN = 10_000       # 1만 원


# ---------------------------------------------------------------------------
# 1. 100만 유저 확보 퍼널 (5억 원 · 12개월)
# ---------------------------------------------------------------------------

@dataclass
class PaidMarket:
    name: str
    budget: int            # 원
    cost_per_user: int     # 스캔 완료 1명당 비용 (원) — 웹 스캔, 앱 설치 불필요

    @property
    def users(self) -> int:
        return self.budget // self.cost_per_user


@dataclass
class FunnelScenario:
    label: str
    paid: list
    creator_users: int     # 성과형 크리에이터 (CPA 정산)
    station_users: int     # 오프라인 Velocity Station 스캔
    public_users: int      # 지자체·보건소·공단 시범사업 연계
    organic_users: int     # PR·검색·ASO
    k_factor: float        # 바이럴 계수 (결과 카드 공유 1회당 신규 스캔 유저)

    @property
    def paid_users(self) -> int:
        return sum(m.users for m in self.paid)

    @property
    def seed_users(self) -> int:
        return (self.paid_users + self.creator_users + self.station_users
                + self.public_users + self.organic_users)

    @property
    def viral_users(self) -> int:
        return self.total_users - self.seed_users

    @property
    def total_users(self) -> int:
        # 기하급수 합: seed × (1 + k + k² + …) = seed / (1 - k)
        return int(self.seed_users / (1 - self.k_factor))


BASE_PAID = [
    PaidMarket("한국", int(1.0 * EOK), 900),
    PaidMarket("일본", int(0.5 * EOK), 1_800),
    PaidMarket("미국", int(0.6 * EOK), 2_300),
]

SCENARIOS = {
    "bear": FunnelScenario(
        "보수", [PaidMarket(m.name, m.budget, int(m.cost_per_user * 1.4)) for m in BASE_PAID],
        creator_users=40_000, station_users=60_000, public_users=15_000,
        organic_users=30_000, k_factor=0.35),
    "base": FunnelScenario(
        "기본", BASE_PAID,
        creator_users=60_000, station_users=100_000, public_users=30_000,
        organic_users=50_000, k_factor=0.60),
    "bull": FunnelScenario(
        "공격", [PaidMarket(m.name, m.budget, int(m.cost_per_user * 0.85)) for m in BASE_PAID],
        creator_users=80_000, station_users=130_000, public_users=40_000,
        organic_users=60_000, k_factor=0.65),
}

MAU_RATIO = 0.22           # 누적 유저 대비 MAU 목표

# 월별 시드 유입 가중치 — M1~M2는 Gate 0 테스트 구간이라 작게 시작
MONTH_WEIGHTS = [1, 2, 5, 7, 9, 10, 11, 11, 11, 11, 11, 11]


def monthly_cumulative(s: FunnelScenario) -> list:
    total_w = sum(MONTH_WEIGHTS)
    out, acc = [], 0
    for w in MONTH_WEIGHTS:
        acc += s.total_users * w / total_w
        out.append(int(acc))
    return out


# ---------------------------------------------------------------------------
# 2. 5억 원 사용처 (v3 대비 재설계)
# ---------------------------------------------------------------------------

BUDGET_V4 = [
    ("그로스 마케팅", "유료 광고 KR·JP·US 2.1억 + 크리에이터 0.3억 + PR 0.1억", int(2.5 * EOK)),
    ("인력", "AI 엔지니어 1 · 그로스 마케터 1 (12개월)", int(1.4 * EOK)),
    ("현지화", "일본어·영어 UX, 현지 결제·약관·개인정보 대응", int(0.4 * EOK)),
    ("인프라·보안", "온디바이스 추론 + 100만 유저 서버·암호화", int(0.35 * EOK)),
    ("IP·규제", "PCT 2건, 광고 문구·웰니스 규제 검토", int(0.35 * EOK)),
]
BUDGET_V3 = [("인건비", 3.0), ("임상 검증", 0.75), ("영업·마케팅", 0.6),
             ("인프라·보안", 0.4), ("IP·법무", 0.25)]

GATES = [
    ("Gate 0", "D+60", "테스트 3,000만 원", "스캔 1명당 비용 ≤ 1,200원 · K ≥ 0.30"),
    ("Gate 1", "M3", "누적 집행 1.5억", "누적 10만 · 4주 재측정률 ≥ 20%"),
    ("Gate 2", "M6", "누적 집행 3.0억", "누적 35만 · Station 100곳"),
    ("Gate 3", "M12", "5억 전액", "누적 100만 · MAU 22만 → 후속 라운드"),
]


# ---------------------------------------------------------------------------
# 3. 건강보험공단 성과공유 모델 (V-SIB)
# ---------------------------------------------------------------------------

@dataclass
class NhisModel:
    cohort: int = 100_000                 # 예방형 위험군 참여자
    onset_rate: float = 0.035             # 연간 고혈압·당뇨 신규 발병률 (가정)
    reduction: float = 0.15               # 조기개입 발병 감소율 (보수 가정)
    cost_per_patient: int = 700_000       # 1인 연 진료비 (가정)
    years: int = 5
    base_fee: int = 3_000                 # 1인·연 기본 운영수수료
    gain_share: float = 0.30              # 검증된 절감액 중 Phydrion 몫

    @property
    def avoided_per_year(self) -> int:
        return int(self.cohort * self.onset_rate * self.reduction)

    def yearly_savings(self) -> list:
        # 회피된 발병자는 해마다 누적된다 (t년차 = t × 연간 회피자)
        return [self.avoided_per_year * t * self.cost_per_patient
                for t in range(1, self.years + 1)]

    @property
    def total_savings(self) -> int:
        return sum(self.yearly_savings())

    @property
    def phydrion_fee(self) -> int:
        return self.cohort * self.base_fee * self.years

    @property
    def phydrion_share(self) -> int:
        return int(self.total_savings * self.gain_share)

    @property
    def phydrion_revenue(self) -> int:
        return self.phydrion_fee + self.phydrion_share

    @property
    def nhis_net(self) -> int:
        return self.total_savings - self.phydrion_revenue

    @property
    def nhis_roi(self) -> float:
        return self.total_savings / self.phydrion_revenue


@dataclass
class P2DModel:
    """검진 결과지·진료 서류 자동 디지털화(특허 P-03)로 줄이는 처리 비용."""
    docs_per_year: int = 5_000_000
    manual_cost: int = 2_000
    auto_cost: int = 300
    phydrion_fee: int = 200

    @property
    def saving(self) -> int:
        return self.docs_per_year * (self.manual_cost - self.auto_cost)

    @property
    def revenue(self) -> int:
        return self.docs_per_year * self.phydrion_fee


# ---------------------------------------------------------------------------
# 4. 앱 밖의 매출 — 3개년 목표
# ---------------------------------------------------------------------------

YEARS = ["2027", "2028", "2029"]
CUM_USERS = [1_000_000, 2_200_000, 4_000_000]


@dataclass
class Stream:
    name: str
    note: str
    values: list = field(default_factory=list)


def revenue_streams() -> list:
    half = [0.5, 1.0, 1.0]   # 2027은 하반기부터 본격 반영

    premium = Stream("B2C 프리미엄", "결제 전환 1→2→2.5% × 연 3.9만 원",
                     [int(u * c * 39_000 * h) for u, c, h in zip(CUM_USERS, [0.01, 0.02, 0.025], half)])
    station = Stream("Velocity Station", "설치 200→800→2,000곳 × 월 5.9만 원",
                     [int(n * 59_000 * 12 * a) for n, a in zip([200, 800, 2_000], [0.5, 0.75, 0.8])])
    vlab = Stream("V-Lab 효능검증", "프로젝트 4→15→35건 × 평균 6,000만 원",
                  [n * 60_000_000 for n in [4, 15, 35]])
    commerce = Stream("Velocity Commerce", "구매 2→3→3.5% × 4.5만 원 × 연 2회 × 수수료 15%",
                      [int(u * b * 45_000 * 2 * 0.15 * h) for u, b, h in zip(CUM_USERS, [0.02, 0.03, 0.035], half)])
    public = Stream("공단·지자체·보험", "V-SIB 시범 → 지자체 확대 → 보험사 연동",
                    [int(0.5 * EOK), 5 * EOK, 15 * EOK])
    return [premium, station, vlab, commerce, public]


def revenue_totals() -> list:
    streams = revenue_streams()
    return [sum(s.values[i] for s in streams) for i in range(len(YEARS))]


# ---------------------------------------------------------------------------
# 5. 마중물 투자자의 지분 가치 (예시)
# ---------------------------------------------------------------------------

SEED_AMOUNT = 5 * EOK
SEED_POST_CAP = 50 * EOK
FOLLOW_ON_RAISE = 30 * EOK
FOLLOW_ON_PRE = [150 * EOK, 250 * EOK, 400 * EOK]


def step_up_table() -> list:
    stake = SEED_AMOUNT / SEED_POST_CAP
    rows = []
    for pre in FOLLOW_ON_PRE:
        post = pre + FOLLOW_ON_RAISE
        diluted = stake * pre / post
        value = diluted * post
        rows.append((pre, post, diluted, value, value / SEED_AMOUNT))
    return rows


# ---------------------------------------------------------------------------

def eok(v: float, digits: int = 1) -> str:
    s = f"{v / EOK:,.{digits}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return f"{s}억"


def man(v: int) -> str:
    return f"{v / MAN:,.0f}만"


if __name__ == "__main__":
    for key, s in SCENARIOS.items():
        print(f"[{s.label}] 유료 {s.paid_users:,} · 시드 {s.seed_users:,} · "
              f"바이럴 {s.viral_users:,} · 합계 {s.total_users:,}")
    print("월별 누적(기본):", [f"{v:,}" for v in monthly_cumulative(SCENARIOS['base'])])
    print("예산 합계:", eok(sum(b[2] for b in BUDGET_V4)))
    n = NhisModel()
    print(f"공단 5년 절감 {eok(n.total_savings)} · Phydrion 매출 {eok(n.phydrion_revenue)} · "
          f"공단 순절감 {eok(n.nhis_net)} · ROI {n.nhis_roi:.2f}x")
    p = P2DModel()
    print(f"P2D 절감 {eok(p.saving)} · 수수료 {eok(p.revenue)}")
    for s in revenue_streams():
        print(s.name, [eok(v) for v in s.values])
    print("합계", [eok(v) for v in revenue_totals()])
    for row in step_up_table():
        print(f"pre {eok(row[0])} → 지분 {row[2]:.1%} · 가치 {eok(row[3])} ({row[4]:.1f}x)")
