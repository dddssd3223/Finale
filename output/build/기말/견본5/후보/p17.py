# -*- coding: utf-8 -*-
# 견본5 기말 모의고사 17번 Claude 후보 (claude17, 5.2점)
# 원본 I37 (2024 수능특강 [24009-0150], Level Up, 원본 난도 6) · 축 ①(설정 유지 · 판정 원리 교체)
# 설정 유지: f(0)=0, 최고차항의 계수의 절댓값 4인 이차함수, a>1, 절댓값 적분 등식 → f=-4x(x-1)
# 원리 교체: [0,a]와 x=1/2 대칭 구간의 적분이 같음 → [0,a]와 겹치는 구간 [a-2,a]의 넓이 S, 겹친 부분 떼기 + 구간 위치로 경우 나누기
ITEMS = {
  17: dict(body=r"""최고차항의 계수의 절댓값이 \(4\)이고 \(f(0)=0\)인 이차함수 \(f(x)\)가 있다. \(1\)보다 큰 실수 \(a\)에 대하여 곡선 \(y=f(x)\)와 \(x\)축 및 두 직선 \(x=a-2\), \(x=a\)로 둘러싸인 부분의 넓이를 \(S\)라 하자. 함수 \(f(x)\)와 \(a\)가 다음 조건을 만족시킬 때, \(a\)의 최댓값은?""",
           cond=[('가', r"""\(\displaystyle\int_0^a|f(x)|\,dx=\int_0^1 f(x)\,dx-\int_1^a f(x)\,dx\)"""),
                 ('나', r"""\(\displaystyle\left|\int_0^a f(x)\,dx\right|\le S\)""")],
           choices=['2', '\\dfrac52', '3', '\\dfrac72', '4'],
           ans=4,
           key='I37', src='2024년 수능특강 [24009-0150]', author='claude', cand='claude17',
           level='상',
           core=dict(axis='①',
                     setting=r"(가)의 절댓값 적분 등식에서 닫힌구간 \([0,1]\)에서 \(f(x)\ge0\), 닫힌구간 \([1,a]\)에서 \(f(x)\le0\)이므로 \(f(1)=0\)이고, \(f(0)=0\)과 최고차항의 계수의 절댓값 \(4\)에서 \(f(x)=-4x(x-1)\)이다.",
                     principle=r"(나)의 \(\displaystyle\int_{1-a}^1 f(x)\,dx\)는 구간 \([0,a]\)를 직선 \(x=\frac12\)에 대하여 대칭이동한 구간의 적분이므로 \(\displaystyle\int_0^a f(x)\,dx\)와 같고, \(|I|\le I\)에서 \(\displaystyle\int_0^a f(x)\,dx\ge0\), 즉 \(a\le\frac32\)이므로 경계 \(a=\frac32\)에서 \(f(a)\)가 최소이다.",
                     new=r"(나)의 두 구간 \([0,a]\), \([a-2,a]\)는 대칭이 아니라 겹친다. 겹친 부분을 떼어 \(\displaystyle\int_0^a f=\int_0^{a-2}f+\int_{a-2}^a f\)로 쓰면, \(a&lt;2\)는 \([0,a]\)가 \([a-2,a]\)에 포함되어 저절로, \(2\le a&lt;3\)은 \(\displaystyle\int_0^{a-2}f\ge0\)이고 \(\displaystyle-\int_{a-2}^a f\le S\)여서 저절로 성립한다. 구간 \([a-2,a]\)가 \(x=1\)의 오른쪽으로 벗어난 \(a\ge3\)에서만 \(\displaystyle S=-\int_{a-2}^a f\)가 되어 (나) \(\Leftrightarrow\displaystyle\int_0^{a-2}f\ge0\Leftrightarrow a-2\le\frac32\)이다."),
           var=r"[판정 원리 교체] (나) \(\left|\int_0^a f\right|\le\int_{1-a}^1 f\)(\(x=\frac12\) 대칭으로 \(\int_0^a f\ge0\)) → \(\left|\int_0^a f\right|\le S\)(\(S\): 구간 \([a-2,a]\)에서 곡선과 \(x\)축 사이의 넓이, 겹친 부분 떼기와 구간 위치에 따른 경우 3가지), (가) 두 등식 → 한 등식(등호 조건으로 부호 결정), \(f(a)\)의 최솟값 → \(a\)의 최댓값",
           sol=r"(가)에서 \(\displaystyle\int_0^a|f(x)|\,dx=\int_0^1|f(x)|\,dx+\int_1^a|f(x)|\,dx\)이고 \(\displaystyle\int_0^1|f(x)|\,dx\ge\int_0^1 f(x)\,dx\), \(\displaystyle\int_1^a|f(x)|\,dx\ge-\int_1^a f(x)\,dx\)이므로 두 부등식에서 모두 등호가 성립해야 한다. 즉 닫힌구간 \([0,1]\)에서 \(f(x)\ge0\), 닫힌구간 \([1,a]\)에서 \(f(x)\le0\)이므로 \(f(1)=0\)이다. \(f(0)=0\)이고 최고차항의 계수의 절댓값이 \(4\)이며 \([0,1]\)에서 \(f(x)\ge0\)이므로 \(f(x)=-4x(x-1)\)이다.<br>"
               r"\(\displaystyle F(x)=\int_0^x f(t)\,dt=2x^2-\frac43x^3=\frac23x^2(3-2x)\)라 하면 \(x\ge0\)에서 \(F(x)\ge0\Leftrightarrow x\le\frac32\)이고, \(x>1\)에서 \(F(x)\)는 감소한다. 또 \(\displaystyle S=\int_{a-2}^a|f(x)|\,dx\)이다.<br>"
               r"(i) \(1&lt;a&lt;2\)일 때: \(a-2&lt;0\)이므로 구간 \([0,a]\)는 구간 \([a-2,a]\)에 포함되고 \(\displaystyle\left|\int_0^a f(x)\,dx\right|\le\int_0^a|f(x)|\,dx\le\int_{a-2}^a|f(x)|\,dx=S\)이다. 따라서 (나)가 성립한다.<br>"
               r"(ii) \(a\ge2\)일 때: \(\displaystyle\int_0^a f(x)\,dx=F(a)\le F(2)=-\frac83&lt;0\)이므로 \(\displaystyle\left|\int_0^a f(x)\,dx\right|=-\int_0^{a-2}f(x)\,dx-\int_{a-2}^a f(x)\,dx=-F(a-2)-\int_{a-2}^a f(x)\,dx\)이고, \(\displaystyle-\int_{a-2}^a f(x)\,dx\le\int_{a-2}^a|f(x)|\,dx=S\)이다.<br>"
               r"\(2\le a&lt;3\)이면 \(0\le a-2&lt;1\)이므로 \(F(a-2)\ge0\)이고 \(\displaystyle\left|\int_0^a f(x)\,dx\right|\le S\)가 성립한다.<br>"
               r"\(a\ge3\)이면 \(a-2\ge1\)이므로 구간 \([a-2,a]\)에서 \(f(x)\le0\)이고 \(\displaystyle S=-\int_{a-2}^a f(x)\,dx\)이다. 따라서 (나)는 \(-F(a-2)+S\le S\), 즉 \(F(a-2)\ge0\)이므로 \(a-2\le\frac32\), \(a\le\frac72\)이다.<br>"
               r"(i), (ii)에서 (나)를 만족시키는 \(a\)의 값의 범위는 \(1&lt;a\le\frac72\)이다. \(a=\frac72\)일 때 \(F\left(\frac32\right)=0\)이므로 \(\displaystyle\left|\int_0^{\frac72}f(x)\,dx\right|=S=\frac{98}{3}\)으로 등호가 성립한다. 따라서 \(a\)의 최댓값은 \(\frac72\)이다.",
           fast=r"\(f(x)=-4x(x-1)\). 구간 \([0,a]\)와 \([a-2,a]\)는 겹치므로 \(\displaystyle\int_0^a f=\int_0^{a-2}f+\int_{a-2}^a f\)로 떼어 본다. \(a\ge3\)이면 \([a-2,a]\)에서 \(f\le0\)이라 \(\displaystyle\int_{a-2}^a f=-S\)이고 (나)는 \(\displaystyle\left|\int_0^{a-2}f-S\right|\le S\Leftrightarrow0\le\int_0^{a-2}f\le2S\)이다. \(\displaystyle\int_0^{a-2}f\le\frac23&lt;S\)라 뒤쪽은 저절로 성립하고, 앞쪽은 넓이가 같아지는 점 \(x=\frac32\)(근 \(0\), \(1\)에서 \(1+\frac12\))에서 \(a-2\le\frac32\)이다. \(a&lt;3\)이면 구간 \([a-2,a]\)에 \(f>0\)인 부분이 들어와 \(S\)가 \(\displaystyle-\int_{a-2}^a f\)보다 커지므로 (나)는 저절로 성립한다. 최댓값 \(\frac72\).",
           wrong=r"① \(2\): (나)의 \(\left|\int_0^a f(x)\,dx\right|\)를 넓이 \(\int_0^a|f(x)|\,dx\)로 혼동하면 \(a\ge2\)에서 \(\int_0^{a-2}|f(x)|\,dx\le0\)이어야 하므로 \(a\le2\)로 얻는 값 / "
                 r"② \(\frac52\): \(F(x)\)를 \(2x^2-4x^3\)으로 잘못 적분해(\(\frac13\) 누락) \(F(x)\ge0\Leftrightarrow x\le\frac12\)로 보면 \(a-2\le\frac12\)에서 얻는 값 / "
                 r"③ \(3\): \(\int_0^{a-2}f(x)\,dx\ge0\)을 (가)처럼 구간 \([0,a-2]\)에서 \(f(x)\ge0\)으로 읽어 \(a-2\le1\)로 얻는 값(구간 \([a-2,a]\)가 \(x=1\)을 지나는 \(a&lt;3\)까지만 보고 \(a\ge3\)을 빠뜨려도 같은 값) / "
                 r"⑤ \(4\): 넓이가 근 \(x=1\)에 대하여 대칭이라고 보아 \(\int_0^2 f(x)\,dx=0\), 즉 넓이가 같아지는 점을 \(x=2\)로 잡아 \(a-2\le2\)로 얻는 값",
           note=r"원본은 (나)의 두 구간 \([0,a]\), \([1-a,1]\)이 \(x=\frac12\)에 대하여 대칭이라 두 적분이 같고, \(|I|\le I\)에서 \(\int_0^a f\ge0\)(\(a\le\frac32\))로 끝났다. 변형의 \(S\)는 구간 \([a-2,a]\)의 넓이라 \([0,a]\)와 겹칠 뿐 대칭이 아니므로 대칭이동이 쓰이지 않고, 원본 결론 \(a\le\frac32\)도 틀린다(\(a=3\)에서도 (나) 성립). 겹친 부분을 떼어 \(\int_0^{a-2}f\)의 부호로 바꾸고, 구간 \([a-2,a]\)가 원점·\(x=1\)을 포함하는지로 경우를 나눠야 하며, 경계 \(a=\frac72\)에서 등호가 성립해 최댓값이 존재한다. (가)는 두 등식을 한 등식으로 묶어 등호 조건으로 부호 구간을 읽게 했다."),
}
