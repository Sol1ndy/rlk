# @s = 아이템, at @s. 가장 가까운 플레이어 시점 기준 버튼 좌우 배치
execute store result storage rlk:dtmp dg int 1 run scoreboard players get @s dgid
execute positioned ~ ~0.9 ~ rotated as @p positioned ^0.95 ^0 ^0 run function rlk:ditem/btn_tp_r with storage rlk:dtmp
execute positioned ~ ~0.9 ~ rotated as @p positioned ^-0.95 ^0 ^0 run function rlk:ditem/btn_tp_s with storage rlk:dtmp
