# 1단계 패링의 접점(p1; 머리 위 · 오른쪽으로 비켜 카메라에서 보이는 자리, fx/p1): 주황 불꽃 0.6칸(round W, 검토 T3-05: 0.3칸 흰 점은 머리 뒤에
# 가려 보이지 않았다; 2단계보다 작고 색이 다르다). 소리(round W: 「패링 단계 전체적으로 효과음이 부실」 — 예전의 사슬 "틱" 하나는 그녀의 신호음보다도
# 작았다): 가볍고 높은 쇳소리 — 삼지창이 돌에 맞는 "칭" + 사슬 끊김 + 작은 모루(짧은 울림 0.15초). 2단계보다 3 dB 쯤 작고 높다
function rlk:player/def/fx/g/spark {s:1.5,c:"#FFA04A"}
particle minecraft:wax_on ~ ~ ~ 0.06 0.06 0.06 2 3 force @a[tag=player]
particle minecraft:dust{color:[1f,0.95f,0.6f],scale:0.5f} ~ ~ ~ 0.1 0.1 0.1 0 3 force @a[tag=player]
playsound minecraft:item.trident.hit_ground player @a[tag=player] ~ ~ ~ 1.1 1.8
playsound minecraft:block.chain.break player @a[tag=player] ~ ~ ~ 2 1.3
playsound minecraft:block.anvil.land player @a[tag=player] ~ ~ ~ 0.9 2
