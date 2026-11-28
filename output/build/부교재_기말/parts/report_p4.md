# Part 4: 05 도함수의 활용(2), printed p.119–131 (M39–M68)

p.119: M39–M40 (Level Up, continued from p.118). p.120–131: M41–M68 (평가원 기출). No figures on any of these pages (figs_p4.py draws nothing).
Column order on p.120–121 is column-major (41,42 left; 43,44 right / 45,46 left; 47,48 right); keys follow printed numbers.

All 30 official answers verified by independent solution (sympy/numeric brute force for M56, M57, M58, M61, M65, M68). No MISMATCH.

Transcription notes:
- M65: book prints the lower branch as `-f(x)+2f(x)` (typo, makes g≡f and the problem meaningless). Transcribed as the original exam `-f(x)+2f(t)`; answer 58 verified with that reading.
- M62: book prints "각각 α, β라 할 때. α−β=…" (period typo); transcribed with a comma as in the original exam.

| key | answer (official) | check | diff | figure | section |
|---|---|---|---|---|---|
| M39 | ③ | OK — f=x⁴+ax³+bx²; b=0이면 f=x³(x+a): h는 극솟값과 0에서만 불연속, h(0±)=2, h(0)=1 → 합 5; 극솟값 -27a⁴/256=-27 → a=±4, f(1)<1 → a=-4, f(1)=-3 | 7 | no | Level Up |
| M40 | ④ | OK — f-f(1)=c(x-1)(x-2)(x-a), f'(1)=f'(a) → a=3; f'max=-c=1 → c=-1; (다) f(0)+f'(0)·(-1)=0 → d=-17; f(-1)=24-17=7 | 6 | no | Level Up |
| M41 | ④ | OK — f'=3x(x-2): m=f(2)=a-4, M=f(4)=a+16 → 2a+12=20, a=4 | 2 | no | 평가원 기출 |
| M42 | ④ | OK — k=-x³+3x²+9x, 극값 -5(x=-1), 27(x=3) → 합 22 | 3 | no | 평가원 기출 |
| M43 | 7 | OK — k=-2x³+6x², x>0에서 0↗8↘ → 0<k<8, 정수 7개 | 3 | no | 평가원 기출 |
| M44 | ③ | OK — k=-x³+3x²-1, 극값 -1, 3 → 양수 k=3 | 3 | no | 평가원 기출 |
| M45 | 15 | OK — f'=6(x+2)(x-1): f(-2)=12, f(1)=-15, f(2)=-4 → max|f|=15 | 3 | no | 평가원 기출 |
| M46 | 8 | OK — a=6t-10 → t=3에서 8 | 1 | no | 평가원 기출 |
| M47 | ② | OK — v=-2t+4=0 → a=2 | 2 | no | 평가원 기출 |
| M48 | 27 | OK — 3t²-4t+3=2t+12 → t=3; x₁=18, x₂=45 → 27 | 3 | no | 평가원 기출 |
| M49 | ③ | OK — -a=2x³+6x²: [-2,0]에서 8↘0, [0,2]에서 0↗40 → 0<-a≤8, 정수 a 8개 | 4 | no | 평가원 기출 |
| M50 | ① | OK — v(1)=0: 3+2a+b=0, a(2)=12+2a=0 → a=-6, b=9 → 3 | 3 | no | 평가원 기출 |
| M51 | ① | OK — t³-6t²+t-6=(t-6)(t²+1)=0 → t=6; p=2, q=-22 → 24 | 3 | no | 평가원 기출 |
| M52 | ② | OK — v=3(t-2)(t+1) → t=2, a=6t-3=9 | 3 | no | 평가원 기출 |
| M53 | ⑤ | OK — x(1)=0(ㄱ 거짓), v(1)=0(ㄴ 참), 방향 전환 t=1에서 a=4(ㄷ 참) → ㄴ, ㄷ | 3 | no | 평가원 기출 |
| M54 | 65 | OK — (2x-1)²+1=(g-1)²+1 → g=2x 또는 g=2-2x; k=-8x³+12x²-11x∈[-7,0], k=(2-u)/2-u³+3u²-6u∈[-8,1] → m=-8, M=1, 65 | 7 | no | 평가원 기출 |
| M55 | 51 | OK — f=x(ax²+bx+c): c=1, b²=8a, f'(1)=3a+2b+1=1 → a=32/9, b=-16/3 → f(3)=3(9a+3b+1)=51 | 6 | no | 평가원 기출 |
| M56 | 21 | OK — f+x=x(x²-9x+22)/2 부호=x 부호: x≥0에서 k=x³-9x²+15x, x<0에서 k=-7x → 4근 k=1..6, 합 21 | 6 | no | 평가원 기출 |
| M57 | 61 | OK — f=a(x-p)²(x-q); x-f(x)=p 또는 q, 하나가 접해야 함; x=1에서 접선 y=x+3 → p=-3, a=-1/16, q=5 → f(0)=45/16, 61 | 8 | no | 평가원 기출 |
| M58 | 14 | OK — (가) ⇔ f(2p)=q-4p³<0; (나) 최댓값 비교 경우 나눔 → 14쌍 (전수검사 확인) | 8 | no | 평가원 기출 |
| M59 | 296 | OK — f=x³+ax²+bx+c: 좌 ⇔ 3x²+2ax+b+4≥0 → a²≤3b+12; 우 ⇔ x⁴-4x²-2ax≥b → b≤-4-2√2|a| → b=-4, a=0 → f'(10)=296 | 7 | no | 평가원 기출 |
| M60 | ③ | OK — a>b>3: ㄱ 판별식 a²-3b>0 참; ㄴ f'(-1)=3-2a+b 음수 가능 거짓; ㄷ 중근 k 2개 + 0근 k 2개 = 4 참 → ㄱ, ㄷ | 6 | no | 평가원 기출 |
| M61 | 40 | OK — 0,a,b 고정점, f(1)=2, f(2)=1(2-주기); f=x+kx(x-a)(x-b) → k=1, {a,b}={3/2,3} → f(5)=5+5·7/2·2=40 | 8 | no | 평가원 기출 |
| M62 | 5 | OK — f=x²(x-c), g=-(x-2)²; (나) c∈{0,2,18}, (다) → c=0, f=x³; k≤x²+2/x → α=3, k≥4-(x+2/x) → β=4-2√2 → α-β=-1+2√2, 5 | 8 | no | 평가원 기출 |
| M63 | 19 | OK — a=3 (x<1에서 g 범위 (3,∞)); f=(x-2)²(x-5)+3 (극대 3, 극소 -1, f(1)=-1) → g(-1)=6, g(6)=19 | 8 | no | 평가원 기출 |
| M64 | 38 | OK — f=-p(x+1)²+q, g=(2p/9)x³-2px+w (근의 합 0-2+3=1); 최대 w+p, 최소 w-4√3p/3 → p=3; h'(-3)=12, h'(4)=26 → 38 | 7 | no | 평가원 기출 |
| M65 | 58 | OK — f=(x-3)²(x-k)+8 (k>3); 불연속점 2개 조건 → k=6 (수치 확인), f(8)=25·2+8=58. 교재 인쇄 '2f(x)'는 '2f(t)' 오타 | 9 | no | 평가원 기출 |
| M66 | ② | OK — f=-px²+15x+7; g'(x≤0) 두 음근 r₁,r₂(a>3√5), g'(x>0) 근 s; r₁+4=r₂, r₂+4=s → r=-5,-1, a=9, s=3, p=5/2 → 5+27=32 | 6 | no | 평가원 기출 |
| M67 | 108 | OK — 단순근 c에서 극한식 불연속 → f(c-3)=0 필요 → f=(x-d)²(x-d-3); g=0 근 d, d+2, d+3, d+6 합 4d+11=7 → d=-1, f(5)=36·3=108 | 9 | no | 평가원 기출 |
| M68 | 483 | OK — 짝수 정수근·홀수 정수근 필요; f=x(x-1)(x+5/8) (f'(-1/4)=-1/4, f'(1/4)<0, 조건 전수확인) → f(8)=8·7·69/8=483 | 9 | no | 평가원 기출 |
