# 0.5칸 전진 → 벽·적 확인 (남은 횟수 #as)
execute if score #jend tmp matches 1 run return 0
execute if score #as tmp matches ..0 run return 0
scoreboard players remove #as tmp 1
tp @s ^ ^ ^0.5
# 기본 공격 화살의 불티 꼬리(0.5칸마다)
execute if score @s aKind matches 1 at @s run particle minecraft:dust{color:[1.0,0.86,0.45],scale:0.5} ~ ~ ~ 0 0 0 0 1
execute if score @s aKind matches 5 at @s run particle minecraft:dust{color:[1.0,0.42,0.12],scale:0.65} ~ ~ ~ 0 0 0 0 1
execute if score @s aKind matches 7 at @s run particle minecraft:dust{color:[0.88,0.15,0.30],scale:0.7} ~ ~ ~ 0.02 0.02 0.02 0 1
execute if score @s aKind matches 8 at @s run function rlk:char/ronova/echo_trail
execute at @s unless block ~ ~ ~ #rlk:dash_pass run return run function rlk:char/bow/arrow_end
# 판정: 화살 주변 ±0.75칸 상자에 몸이 걸친 적
execute at @s positioned ~-0.75 ~-0.75 ~-0.75 if entity @e[tag=rlk_mob,dx=0.5,dy=0.5,dz=0.5] run return run function rlk:char/bow/arrow_hit
execute at @s run function rlk:char/bow/arrow_step
