# @s = 오브젝트: 딸린 표시 엔티티까지 제거
scoreboard players operation #g tmp = @s ogid
execute as @e[tag=rlk_room] if score @s ogid = #g tmp run kill @s
