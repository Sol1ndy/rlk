# 명계의 반동 (@s = 플레이어, at 몸): 되살아나는 순간 주변 6칸의 적에게 공허 충격파
function rlk:char/dmg_calc {coef:250}
scoreboard players set #elem tmp 8
scoreboard players set #elU tmp 1000
scoreboard players set #rnErAdd tmp 10
tag @e[tag=rlk_mob,distance=..6] add rlk_hit
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
# 밀쳐냄(보스 제외): 몸에서 먼 쪽으로 세게 + 위로 살짝
scoreboard players operation #kbSave tmp = #kbBasic tmp
scoreboard players operation #kbBasic tmp = #rnRevKb tmp
execute as @e[tag=rlk_hit,tag=!boss] at @s run function rlk:mob/knock
execute as @e[tag=rlk_hit,tag=!boss,tag=!rlk_cm_cn] run data modify entity @s Motion[1] set value 0.38d
scoreboard players operation #kbBasic tmp = #kbSave tmp
tag @e[tag=rlk_hit] remove rlk_hit
function rlk:char/after_hit
# 빈 잔향 칸을 공허 잔향으로
scoreboard players set #rvE tmp 8
function rlk:char/ronova/echo_push
function rlk:char/ronova/echo_push
function rlk:char/ronova/echo_push
# 효과: 붉은 고리가 퍼져 나감 + 바닥의 검붉은 균열
function rlk:char/ronova/rev_fx
