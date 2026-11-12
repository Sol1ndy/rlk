# 2단계 패링의 접점(p2; 머리 위 · 오른쪽으로 비켜 카메라에서 보이는 자리, fx/p2): 노란 흰 불꽃 0.8칸 + 튀는 불티(round W, 검토 T3-05:
# 0.45칸은 5~10 px 로 머리 뒤에 가려졌다; 퍼펙트의 1.3칸 별빛 · 화면 연출과는 여전히 다르다). 소리(round W): 단단한 쇠 부딪힘 — 모루(1.5배 높이, 울림 0.3초) + 삼지창 "칭" + 철 골렘의
# 금 가는 소리(몸통) + 옅은 "딩". 퍼펙트보다 4~5 dB 작고(싸움의 큰 소리 −28 dBFS 쯤과 같거나 큼) 붐 · 긴 울림 · 풀림 소리가 없다(「막았지만 퍼펙트는 아니다」)
function rlk:player/def/fx/g/spark {s:2.0,c:"#FFF4B0"}
particle minecraft:dust{color:[1f,0.95f,0.6f],scale:0.6f} ~ ~ ~ 0.12 0.12 0.12 0 4 force @a[tag=player]
particle minecraft:wax_off ~ ~ ~ 0.08 0.08 0.08 3 8 force @a[tag=player]
playsound minecraft:block.anvil.land player @a[tag=player] ~ ~ ~ 1.6 1.5
playsound minecraft:item.trident.hit_ground player @a[tag=player] ~ ~ ~ 1.1 1.5
playsound minecraft:entity.iron_golem.damage player @a[tag=player] ~ ~ ~ 0.7 1.5
playsound minecraft:entity.arrow.hit_player player @a[tag=player] ~ ~ ~ 0.35 1.04
