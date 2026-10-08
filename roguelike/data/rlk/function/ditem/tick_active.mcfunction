# 드롭 아이템 처리 본체 (rlk_ditem 존재 시에만 호출됨). aimingDrop 리셋은 상위 ditem/tick에서 매 틱 수행
scoreboard players set #aimedGid tmp 0
tag @e[tag=rlk_dbtn] remove rlk_dhover
execute as @e[tag=rlk_ditem] at @s run function rlk:ditem/btn_face
execute as @a[tag=player] at @s anchored eyes run function rlk:ditem/aim
execute as @e[tag=rlk_dinfo] run function rlk:ditem/disp
execute as @e[tag=rlk_dbtn] at @s run function rlk:ditem/btn
execute as @e[tag=rlk_dbtn] at @s run function rlk:ditem/btn_hover
execute as @e[tag=rlk_daura] at @s run function rlk:ditem/aura
