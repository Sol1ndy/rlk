# @s = 조준 중인 오브젝트, at @s. 좌클릭 처리 (일반 공격으로 이어지지 않게 #shopHandled)
scoreboard players set #shopHandled tmp 1
execute if score #combat room matches 1.. run return 0
execute if score @s oact matches 1 run return run function rlk:room/obj/do_money
execute if score @s oact matches 2 run return run function rlk:room/obj/do_sapphire
execute if score @s oact matches 3 run return run tellraw @a[tag=player] [{"text":"상인: ","color":"#6FCF8F"},{"text":"아직 물건을 들여오는 중이라네. (준비 중)","color":"gray"}]
execute if score @s oact matches 4 run return run tellraw @a[tag=player] [{"text":"[재련] ","color":"#C9C9C9"},{"text":"아직 사용할 수 없습니다. (준비 중)","color":"gray"}]
execute if score @s oact matches 5 run return run tellraw @a[tag=player] [{"text":"[인챈트] ","color":"#B58BE8"},{"text":"아직 사용할 수 없습니다. (준비 중)","color":"gray"}]
execute if score @s oact matches 6 run return run tellraw @a[tag=player] [{"text":"[나무뿌리] ","color":"#B08A5A"},{"text":"아직 아무 일도 일어나지 않습니다. (준비 중)","color":"gray"}]
execute if score @s oact matches 7 run scoreboard players operation #mapType room = @s oarg
# 재련 맵을 고름 → 고른 횟수 +1
execute if score @s oact matches 7 if score @s oarg matches 6 run scoreboard players add #rfCount room 1
execute if score @s oact matches 7 run return run function rlk:run/next_map
execute if score @s oact matches 8 run return run function rlk:run/next_chapter
