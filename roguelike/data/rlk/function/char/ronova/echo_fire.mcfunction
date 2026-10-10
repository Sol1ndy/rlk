# 잔향 #rvE 발사 (@s = 플레이어, 위치·방향 = 쏠 자리). 공격력의 160% 그 원소(만개 잔향 = 풀), 반경 2.5칸. #pOff: 0 가운데 / 1 오른쪽 / 2 왼쪽
scoreboard players set #coef tmp 160
function rlk:char/bow/calc
scoreboard players set #pKind tmp 8
scoreboard players operation #pEl tmp = #rvE tmp
execute if score #pEl tmp matches 9 run scoreboard players set #pEl tmp 7
scoreboard players set #pIcd tmp 0
scoreboard players set #pBig tmp 0
scoreboard players set #pSub tmp 3
scoreboard players set #pLife tmp 16
# 숄더뷰: 떠 있는 법구에서(지금 방향 그대로, 두 발이면 좌우로 벌림) / 1인칭: 눈앞에서
scoreboard players set #catOn tmp 0
execute unless entity @s[tag=rlk_body] if entity @e[tag=rlk_rncat_c,limit=1] run scoreboard players set #catOn tmp 1
execute if score #catOn tmp matches 1 if score #pOff tmp matches 0 positioned as @e[tag=rlk_rncat_c,limit=1] run function rlk:char/ronova/proj_spawn
execute if score #catOn tmp matches 1 if score #pOff tmp matches 1 positioned as @e[tag=rlk_rncat_c,limit=1] positioned ^-0.3 ^ ^ run function rlk:char/ronova/proj_spawn
execute if score #catOn tmp matches 1 if score #pOff tmp matches 2 positioned as @e[tag=rlk_rncat_c,limit=1] positioned ^0.3 ^ ^ run function rlk:char/ronova/proj_spawn
execute if score #catOn tmp matches 1 run function rlk:char/ronova/cat_flash
execute if score #catOn tmp matches 0 if score #pOff tmp matches 0 positioned ~ ~1.62 ~ positioned ^ ^-0.15 ^0.5 run function rlk:char/ronova/proj_spawn
execute if score #catOn tmp matches 0 if score #pOff tmp matches 1 positioned ~ ~1.62 ~ positioned ^-0.45 ^-0.1 ^0.5 run function rlk:char/ronova/proj_spawn
execute if score #catOn tmp matches 0 if score #pOff tmp matches 2 positioned ~ ~1.62 ~ positioned ^0.45 ^-0.1 ^0.5 run function rlk:char/ronova/proj_spawn
execute unless score #k273 snd matches 1 run function rlk:snd/f308
execute unless score #k274 snd matches 1 run function rlk:snd/f309
