# 퍼펙트 닷지 1~10틱, 몸 둘레를 떠도는 붉은 분홍 불티(위치 = 몸)
particle minecraft:dust{color:[1f,0.45f,0.55f],scale:0.8f} ~ ~1 ~ 0.5 0.75 0.5 0 3 force @a[tag=player]
particle minecraft:dust{color:[1f,0.85f,0.88f],scale:0.5f} ~ ~1 ~ 0.55 0.8 0.55 0 2 force @a[tag=player]
execute if score #btA cb matches 2..9 run particle minecraft:cherry_leaves ~ ~1.4 ~ 0.5 0.4 0.5 0 1 force @a[tag=player]
