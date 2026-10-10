tag @e[tag=rlk_rd_ilact] remove rlk_rd_ilact
execute as @e[tag=rlk_rd_illusion] if score @s rdTurns = #rdIlTurn rd run tag @s add rlk_rd_ilact
# Its illusion was shattered before its turn: skip straight to the next one.
execute unless entity @e[tag=rlk_rd_ilact,limit=1] run return run function rlk:boss/raiden/illusion/turn_skip
scoreboard players set #rdIlShots rd 1
execute if entity @e[tag=rlk_rd_ilact,scores={rdReal=1},limit=1] run scoreboard players set #rdIlShots rd 2
execute as @e[tag=rlk_rd_ilact,limit=1] at @s run function rlk:boss/raiden/illusion/wind {tell:13,life:23}
