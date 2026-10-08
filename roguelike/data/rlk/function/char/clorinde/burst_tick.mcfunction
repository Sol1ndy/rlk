execute if score @s clBurst matches 1 at @e[tag=rlk_clb,limit=1] run function rlk:char/clorinde/burst_hit
execute if score @s clBurst matches 4 at @e[tag=rlk_clb,limit=1] run function rlk:char/clorinde/burst_hit
execute if score @s clBurst matches 7 at @e[tag=rlk_clb,limit=1] run function rlk:char/clorinde/burst_hit
execute if score @s clBurst matches 10 at @e[tag=rlk_clb,limit=1] run function rlk:char/clorinde/burst_hit
execute if score @s clBurst matches 13 at @e[tag=rlk_clb,limit=1] run function rlk:char/clorinde/burst_hit
scoreboard players add @s clBurst 1
execute if score @s clBurst matches 14.. run kill @e[tag=rlk_clb]
execute if score @s clBurst matches 14.. run scoreboard players set @s clBurst 0
