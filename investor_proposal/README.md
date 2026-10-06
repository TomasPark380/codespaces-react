# PHYDRION 마중물 투자 제안서 (v4 보충)

사업계획서 v3에 덧붙이는 설득형 투자 제안서입니다. 전부 Python(reportlab)으로 만듭니다.

| 파일 | 역할 |
|---|---|
| `model.py` | 모든 수치의 가정과 계산 (퍼널, 공단 절감, 매출, 지분 가치) |
| `build_proposal.py` | 16:9 PDF 15페이지 생성 |
| `PHYDRION_Investment_Proposal_v4.pdf` | 생성 결과물 |
| `build_pitch10.py` | 투자 설득용 10장 압축판 생성 (같은 도구·수치 재사용) |
| `PHYDRION_Pitch_10p.pdf` | 10장 압축판 결과물 |

```bash
pip install reportlab koreanize-matplotlib   # 나눔고딕 폰트를 이 패키지에서 가져옴
python model.py            # 핵심 수치 요약 출력
python build_proposal.py   # 15페이지 상세판 다시 생성
python build_pitch10.py    # 10장 압축판 다시 생성
```

가정(광고 단가, K 계수, 발병률, 전환율 등)은 `model.py` 상단에서 바꿉니다. 바꾼 뒤 다시 빌드하면 모든 페이지 수치가 함께 바뀝니다.

## 구성

1. 표지 · 요약 · "미용 동기로 들어와 건강 데이터로 남는다"
2. **제안 1 — 공단의 새 고객군**: V-SIB 성과공유 모델, 위험군 10만 명 5년 절감 시뮬레이션, P2D(특허 P-03) 서류 처리비 절감
3. **제안 2 — 앱 밖의 매출**: Velocity Station · V-Lab 효능검증 · Velocity Commerce · B2E·보험, 3개년 매출 목표
4. **제안 3 — 5억 → 100만 유저**: 퍼널 산식(보수·기본·공격 시나리오), 국가별 집행, 사용처 재설계, 집행 게이트, 월별 로드맵
5. 마중물 논리와 지분 가치 예시 · 예상 질문과 답변 · 다음 단계

## 보내기 전 직접 채워야 할 것

- 후속 투자: 미국 소재 투자회사(사명 비공개), 조건 MAU 30만, 규모 30억 원 내외(협의 중 가정)로 기재됨. 규모가 다르면 `model.py`의 `FOLLOW_ON_RAISE` 수정
- SAFE 조건(Cap 50억, 2회 분할 납입)은 제안안이며 대표 확정이 필요함
- 모든 수치는 검증 전 목표·가설임. 실적(2026-09 기준 매출 0원)은 v3 Part 7 참조
