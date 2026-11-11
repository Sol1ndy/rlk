# Internal (@s = the player): the avatar the actor hid shows again. A rig character's avatar stays hidden under its rig.
execute unless entity @e[tag=rlk_av,tag=rlk_cine_hid,limit=1] run return 0
execute if data storage rlk:cine av run data modify entity @e[tag=rlk_av,limit=1] profile set from storage rlk:cine av
data remove storage rlk:cine av
execute if score @s pmVisible matches 1 run return 0
execute if score @s pmActive matches 1 run return 0
effect clear @e[tag=rlk_av,limit=1] minecraft:invisibility
item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand from entity @s hotbar.0
function rlk:view/av_unwrap
execute if score #charN tmp matches 7..8 run item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand with minecraft:air
