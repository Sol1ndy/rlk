# 퍼펙트 닷지의 잔상 자리(pd): 마네킹 잔상, 섬광, 붉은 고리
execute rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 run function rlk:player/def/fx/pd_ghost
particle minecraft:flash{color:[1f,0.18f,0.12f,1f]} ~ ~1.1 ~ 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust_color_transition{from_color:[1f,0.3f,0.15f],to_color:[0.35f,0f,0.02f],scale:1.4f} ~ ~1 ~ 0.4 0.7 0.4 0 24 force @a[tag=player]
particle minecraft:dust{color:[1f,0.45f,0.2f],scale:1.6f} ~ ~0.1 ~ 0.9 0.02 0.9 0 14 force @a[tag=player]
playsound minecraft:entity.illusioner.mirror_move player @a[tag=player] ~ ~ ~ 0.8 1.3
playsound minecraft:entity.breeze.slide player @a[tag=player] ~ ~ ~ 0.6 0.8
