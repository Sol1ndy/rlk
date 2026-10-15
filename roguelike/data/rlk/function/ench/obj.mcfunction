# 인챈트 오브젝트를 누름 (@s = 오브젝트 표식). 남은 횟수 = oarg. 화면(pkMode 8)으로
scoreboard players operation #enchG room = @s ogid
scoreboard players operation #enchN room = @s oarg
execute as @a[tag=player,limit=1] at @s run function rlk:ench/open
