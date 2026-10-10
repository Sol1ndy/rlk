# Leave joint rotations still while clearing the brief damage flash normally.
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_sw_this] remove rlk_sw_this
