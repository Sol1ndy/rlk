# 결정 축포 (@s = 플레이어, at 몸). #skBtn: 1 = 좌클릭(바로 발사) / 2 = 우클릭(누르고 있는 동안 조준, 떼면 발사)
# 조준 중에 다시 들어온 우클릭 = 아직 누르고 있음
execute if score @s nvA matches 1.. run return run scoreboard players set @s nvGap 0
execute if score @s nvFcd matches 1.. run return 0
execute unless score @s nvC matches 1.. run return run function rlk:char/deny {t:"결정 축포 충전 중"}
execute if score #skBtn tmp matches 2 run return run function rlk:char/navia/aim_start
function rlk:char/navia/fire
