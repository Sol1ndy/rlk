# 달 반응이 일어나거나 달 피해를 줌 (#lnT = 1 달 감전 / 2 달 개화 / 3 달 결정). 아이템 · 캐릭터 효과는 여기에 추가
# 서리달의 은잔: 중력의 물결이 있는 동안 달 반응 → 중력 (중력 간섭 중에는 쌓이지 않음)
execute if score @a[tag=player,limit=1] it_moon_chalice matches 1.. if score #cgRipT itv matches 1.. unless score #cgIn itv matches 1 run function rlk:items/proc/cg_gain
# 각인 만월 4개: 달 반응 → 원소 마스터리
execute if score fullmoon engN matches 4.. run scoreboard players operation #fmT eng = #fmDur tmp
