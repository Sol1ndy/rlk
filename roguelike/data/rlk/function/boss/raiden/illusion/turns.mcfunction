# As the boss. Turn clock 1 = wind-up; fakes slash once, the real one twice.
scoreboard players add #rdIlClock rd 1
# hold() hands over with clock -1: nothing happens on the tick the spots are taken.
execute if score #rdIlClock rd matches ..0 run return 0
execute if score #rdIlClock rd matches 1 run function rlk:boss/raiden/illusion/turn_begin
execute unless score #rdIlStep rd matches 2 run return 0
# A shattered fake simply gives up the rest of its turn.
execute unless entity @e[tag=rlk_rd_ilact,limit=1] run return run function rlk:boss/raiden/illusion/turn_end
execute if score #rdIlClock rd matches 14 as @e[tag=rlk_rd_ilact,limit=1] at @s run function rlk:boss/raiden/illusion/strike
execute if score #rdIlShots rd matches 2 if score #rdIlClock rd matches 17 as @e[tag=rlk_rd_ilact,limit=1] at @s run function rlk:boss/raiden/illusion/wind {tell:9,life:19}
execute if score #rdIlShots rd matches 2 if score #rdIlClock rd matches 26 as @e[tag=rlk_rd_ilact,limit=1] at @s run function rlk:boss/raiden/illusion/strike
execute if score #rdIlShots rd matches 1 if score #rdIlClock rd matches 20.. run return run function rlk:boss/raiden/illusion/turn_end
execute if score #rdIlClock rd matches 32.. run function rlk:boss/raiden/illusion/turn_end
