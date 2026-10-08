# 낙사 구간 매 틱 (런 진행 중). '안전한 자리' 표식(rlk_safe) = 플레이어(몸)가 마지막으로 단단한 바닥을 딛고 있던 곳
execute unless entity @e[tag=rlk_safe,limit=1] at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_safe"]}
execute unless score @a[tag=player,limit=1] dashMoveT matches 1.. at @e[tag=rlk_body,limit=1] if block ~ ~ ~ #rlk:dash_pass positioned ~ ~-0.2 ~ unless block ~ ~ ~ #rlk:dash_pass run tp @e[tag=rlk_safe,limit=1] ~ ~0.2 ~
# 떨어짐: 발이 y 197 아래로 내려간 것 (던전 범위 안)
execute positioned -64 120 -64 if entity @e[tag=rlk_body,dx=127,dy=76,dz=127] as @a[tag=player,limit=1] unless score @s devMode matches 1 run function rlk:room/fall/player
execute positioned -64 120 -64 as @e[tag=rlk_mob,dx=127,dy=76,dz=127] run function rlk:room/fall/mob
# 떨어진 골드·회복 구슬은 안전한 자리로 올려 준다
execute positioned -64 120 -64 as @e[type=minecraft:item,dx=127,dy=76,dz=127] at @e[tag=rlk_safe,limit=1] run tp @s ~ ~0.5 ~
