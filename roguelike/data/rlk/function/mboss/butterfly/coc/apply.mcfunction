# 달빛 고치 on the player (any executor): skipped while the player is dead, reviving or on a selection screen.
execute as @a[tag=player,scores={dead=0},limit=1] unless score @s rnDie matches 1.. unless score @s pkMode matches 1.. at @s run function rlk:mboss/butterfly/coc/apply_pl
