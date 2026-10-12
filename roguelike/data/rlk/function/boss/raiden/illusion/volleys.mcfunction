# As the boss. Three volleys: everyone winds up together and cuts toward the centre;
# fakes once, the real one an X (second diagonal stroke 3 ticks later).
scoreboard players add #rdIlClock rd 1
# hold() hands over with clock -1: nothing happens on the tick the spots are taken.
execute if score #rdIlClock rd matches ..0 run return 0
execute if score #rdIlClock rd matches 1 as @e[tag=rlk_rd_illusion] at @s run function rlk:boss/raiden/illusion/wind {tell:10,life:20}
execute if score #rdIlClock rd matches 11 as @e[tag=rlk_rd_illusion] at @s run function rlk:boss/raiden/illusion/strike
execute if score #rdIlClock rd matches 14 as @e[tag=rlk_rd_illusion,scores={rdReal=1},limit=1] at @s run function rlk:boss/raiden/illusion/strike_x2
execute if score #rdIlClock rd matches 21.. run function rlk:boss/raiden/illusion/volley_end
