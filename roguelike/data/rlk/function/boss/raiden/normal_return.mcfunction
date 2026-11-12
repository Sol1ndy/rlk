# Back to the Shogun (end of the break, or test/to_normal). The forced weapon switch comes next: the Shogun
# choose consumes rlk_rd_switch_due (rd/s2_notes.md §3.2.1).
attribute @s minecraft:scale base set 1.2
kill @e[tag=rlk_rd_tm]
scoreboard players set @s rdPhase 0
scoreboard players set @s rdRage 0
tag @s add rlk_rd_switch_due
tag @s remove rlk_rd_tm_rear
function rlk:boss/raiden/finish
scoreboard players set @s rdCool 20
function rlk:room/raiden/look_shogun
execute if score @s rdRigW matches 1 run function rlk:boss/raiden/rig/play/idle_polearm
execute unless score @s rdRigW matches 1 run function rlk:boss/raiden/rig/play/idle_sword
