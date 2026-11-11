# 2단계 패링의 접점(p2): 작은 불꽃 0.45칸 + 불티. 소리(round W): 단단한 쇠 부딪힘 — 모루(1.5배 높이, 울림 0.3초) + 삼지창 "칭" + 철 골렘의
# 금 가는 소리(몸통) + 옅은 "딩". 퍼펙트보다 4~5 dB 작고(싸움의 큰 소리 −28 dBFS 쯤과 같거나 큼) 붐 · 긴 울림 · 풀림 소리가 없다(「막았지만 퍼펙트는 아니다」)
function rlk:player/def/fx/g/spark {s:1.1}
particle minecraft:dust{color:[1f,0.95f,0.6f],scale:0.6f} ~ ~ ~ 0.12 0.12 0.12 0 4 force @a[tag=player]
particle minecraft:wax_off ~ ~ ~ 0.08 0.08 0.08 1.5 3 force @a[tag=player]
playsound minecraft:block.anvil.land player @a[tag=player] ~ ~ ~ 1.6 1.5
playsound minecraft:item.trident.hit_ground player @a[tag=player] ~ ~ ~ 1.1 1.5
playsound minecraft:entity.iron_golem.damage player @a[tag=player] ~ ~ ~ 0.7 1.5
playsound minecraft:entity.arrow.hit_player player @a[tag=player] ~ ~ ~ 0.35 1.04
