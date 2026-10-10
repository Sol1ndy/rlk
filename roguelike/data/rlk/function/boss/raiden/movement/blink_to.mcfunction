# @s boss; the execution position is the destination (e.g. positioned at the arena centre).
# Scatter blink: depart art where the boss stands, hidden travel, the controller's
# blink_relocate (rdBlink 4) consumes the rlk_rd_blink_dest marker, arrive art there.
kill @e[tag=rlk_rd_blink_dest]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_blink_dest"]}
# A blink that has not relocated yet simply takes the new destination.
execute if score @s rdBlink matches 1..3 run return 0
scoreboard players set @s rdBlink 0
execute at @s run function rlk:boss/raiden/movement/blink_start
