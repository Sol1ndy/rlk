# @s = 플레이어. atkBlock(감쌈, 우클릭 전담) + atkStrike(눈앞, 좌클릭 전담) 유지/추적
scoreboard players operation #mypid tmp = @s pid
# 폴링: atkBlock=우클릭 감지, atkStrike=좌클릭 감지 (각 원자적 제거)
execute as @e[tag=atkBlock] if score @s intOwner = #mypid tmp run function rlk:combat/atkblock_poll
execute as @e[tag=atkStrike] if score @s intOwner = #mypid tmp run function rlk:combat/atkstrike_poll
# 유지해야 하나? (dev/드롭조준 제외)
scoreboard players set #want tmp 1
execute if score @s devMode matches 1 run scoreboard players set #want tmp 0
execute if score @s aimingDrop matches 1 if entity @s[tag=rlk_body] run scoreboard players set #want tmp 0
# 원치 않으면 내 것 제거하고 종료
execute if score #want tmp matches 0 as @e[tag=atkBlock] if score @s intOwner = #mypid tmp run kill @s
execute if score #want tmp matches 0 as @e[tag=atkStrike] if score @s intOwner = #mypid tmp run kill @s
execute if score #want tmp matches 0 run return 0
# atkBlock(우클릭+차단, 5×3): 존재 여부 → tp/재생성
scoreboard players set #has tmp 0
execute as @e[tag=atkBlock] if score @s intOwner = #mypid tmp run scoreboard players set #has tmp 1
execute if score #has tmp matches 1 unless score @s dashMoveT matches 1.. at @s anchored eyes positioned ^ ^ ^ positioned ~ ~-0.75 ~ as @e[tag=atkBlock] if score @s intOwner = #mypid tmp run function rlk:combat/atkblock_follow
execute if score #has tmp matches 1 if score @s dashMoveT matches 1.. at @s anchored eyes positioned ^ ^ ^2 positioned ~ ~-0.75 ~ as @e[tag=atkBlock] if score @s intOwner = #mypid tmp run function rlk:combat/atkblock_follow
execute if score #has tmp matches 0 at @s anchored eyes positioned ^ ^ ^1.65 positioned ~ ~-0.75 ~ run function rlk:combat/atkblock_spawn
# atkStrike(좌클릭 감지, 눈앞 1블록, 작음): atkBlock 표면(2.5)보다 가까워 좌클릭을 먼저 가로챔
scoreboard players set #hasS tmp 0
execute as @e[tag=atkStrike] if score @s intOwner = #mypid tmp run scoreboard players set #hasS tmp 1
execute if score #hasS tmp matches 1 unless score @s dashMoveT matches 1.. at @s anchored eyes positioned ^ ^ ^1 positioned ~ ~-0.5 ~ as @e[tag=atkStrike] if score @s intOwner = #mypid tmp run tp @s ~ ~ ~
execute if score #hasS tmp matches 1 if score @s dashMoveT matches 1.. at @s anchored eyes positioned ^ ^ ^2 positioned ~ ~-0.5 ~ as @e[tag=atkStrike] if score @s intOwner = #mypid tmp run tp @s ~ ~ ~
execute if score #hasS tmp matches 0 at @s anchored eyes positioned ^ ^ ^1 positioned ~ ~-0.5 ~ run function rlk:combat/atkstrike_spawn
