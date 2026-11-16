# @s = player. The stand-in rig goes, the mannequin shows again with its weapon (as char/motion/stop).
scoreboard players set @s plActive 0
kill @e[tag=rlk_pl]
kill @e[tag=rlk_pl_basis]
execute if entity @e[tag=rlk_av,limit=1] run effect clear @e[tag=rlk_av,limit=1] minecraft:invisibility
execute if entity @e[tag=rlk_av,limit=1] run item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand from entity @s hotbar.0
execute if entity @e[tag=rlk_av,limit=1] run function rlk:view/av_unwrap
execute if score #charN tmp matches 7..8 run item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand with minecraft:air
