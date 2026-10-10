# @s = 플레이어. 눈 바로 앞 입력 실드 + 앞쪽 예비 입력 실드를 유지한다.
scoreboard players operation #mypid tmp = @s pid
# 위치 갱신/제거보다 먼저 지난 틱 입력을 소비한다.
execute as @e[tag=atkBlock] if score @s intOwner = #mypid tmp run function rlk:combat/atkblock_poll
execute as @e[tag=atkStrike] if score @s intOwner = #mypid tmp run function rlk:combat/atkstrike_poll
scoreboard players set #want tmp 1
execute if score @s devMode matches 1 run scoreboard players set #want tmp 0
execute if score @s aimingDrop matches 1 if entity @s[tag=rlk_body] run scoreboard players set #want tmp 0
execute if score #want tmp matches 0 as @e[tag=atkBlock] if score @s intOwner = #mypid tmp run kill @s
execute if score #want tmp matches 0 as @e[tag=atkStrike] if score @s intOwner = #mypid tmp run kill @s
execute if score #want tmp matches 0 run return 0
# 가까운 실드: 0.32 정육면체의 중심을 눈앞 0.30에 둔다. 어떤 시선 각도에서도 눈이 내부에 들어가지 않는다.
# 기존 5×3 실드가 눈/몹 몸과 함께 겹쳐 선택되는 상황을 없앤다. 대쉬 중에도 앞쪽 거리를 바꾸지 않는다.
scoreboard players set #has tmp 0
execute as @e[tag=atkBlock] if score @s intOwner = #mypid tmp run scoreboard players set #has tmp 1
execute as @e[tag=atkBlock] if score @s intOwner = #mypid tmp unless data entity @s {width:0.32f,height:0.32f} run data merge entity @s {width:0.32f,height:0.32f}
execute if score #has tmp matches 1 at @s anchored eyes positioned ^ ^ ^0.30 positioned ~ ~-0.16 ~ as @e[tag=atkBlock] if score @s intOwner = #mypid tmp run function rlk:combat/atkblock_follow
execute if score #has tmp matches 0 at @s anchored eyes positioned ^ ^ ^0.30 positioned ~ ~-0.16 ~ run function rlk:combat/atkblock_spawn
# 예비 실드: 1.4 정육면체를 눈앞 1.60에 배치. 빠른 회전/이동 때 가까운 실드를 빗나가도 잡는다.
scoreboard players set #hasS tmp 0
execute as @e[tag=atkStrike] if score @s intOwner = #mypid tmp run scoreboard players set #hasS tmp 1
execute if score #hasS tmp matches 1 at @s anchored eyes positioned ^ ^ ^1.60 positioned ~ ~-0.70 ~ as @e[tag=atkStrike] if score @s intOwner = #mypid tmp run tp @s ~ ~ ~
execute if score #hasS tmp matches 0 at @s anchored eyes positioned ^ ^ ^1.60 positioned ~ ~-0.70 ~ run function rlk:combat/atkstrike_spawn
