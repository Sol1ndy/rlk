# 인챈트 오브젝트를 누름 (@s = 오브젝트 표식). 남은 횟수 = oarg. 화면(pkMode 8)으로
# 업데이트 전에 생긴 인챈트대(oarg 0)는 이때 횟수를 정한다
execute unless score @s oarg matches 1.. store result score @s oarg run random value 2..4
scoreboard players operation #enchG room = @s ogid
scoreboard players operation #enchN room = @s oarg
execute as @a[tag=player,limit=1] at @s run function rlk:ench/open
