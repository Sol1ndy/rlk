# 돌진 한 칸 (@s = 플레이어, 방향 = 수평 시선). 몸(숄더뷰 = 아바타, 1인칭 = 플레이어)을 옮긴다
execute if score #nfDs tmp matches ..0 run return 0
scoreboard players remove #nfDs tmp 1
execute at @e[tag=rlk_body,limit=1] positioned ^ ^ ^1 unless block ~ ~0.1 ~ #rlk:dash_pass run return 0
execute at @e[tag=rlk_body,limit=1] positioned ^ ^ ^1 unless block ~ ~1.1 ~ #rlk:dash_pass run return 0
execute at @e[tag=rlk_body,limit=1] run particle minecraft:composter ~ ~0.6 ~ 0.3 0.4 0.3 0 6
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.45,0.85,0.25],scale:1.3} ~ ~0.8 ~ 0.3 0.4 0.3 0 6
execute if entity @s[tag=rlk_body] at @s positioned ^ ^ ^1 run tp @s ~ ~ ~
execute unless entity @s[tag=rlk_body] as @e[tag=rlk_av,limit=1] at @s positioned ^ ^ ^1 run tp @s ~ ~ ~
execute at @e[tag=rlk_body,limit=1] run tag @e[tag=rlk_mob,distance=..1.8] add rlk_hit
function rlk:char/nefer/dash_step
