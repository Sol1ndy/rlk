# @s = player (a mannequin character; from rlk:char/motion/beat/dodge): play pdodge on the stand-in rig. Nothing in developer mode (no avatar).
execute unless entity @e[tag=rlk_av,limit=1] run return 0
# parts left by another character or an unfinished run are not reused
execute unless score @s plActive matches 1 run kill @e[tag=rlk_pl]
execute if score #charN tmp matches 1 unless entity @e[tag=rlk_pl,limit=1] at @e[tag=rlk_av,limit=1] run function rlk:char/motion/lite/spawn_lumine
execute if score #charN tmp matches 4 unless entity @e[tag=rlk_pl,limit=1] at @e[tag=rlk_av,limit=1] run function rlk:char/motion/lite/spawn_clorinde
execute if score #charN tmp matches 7 unless entity @e[tag=rlk_pl,limit=1] at @e[tag=rlk_av,limit=1] run function rlk:char/motion/lite/spawn_ronova
execute if score #charN tmp matches 8 unless entity @e[tag=rlk_pl,limit=1] at @e[tag=rlk_av,limit=1] run function rlk:char/motion/lite/spawn_nefer
execute unless entity @e[tag=rlk_pl,limit=1] run return 0
scoreboard players set @s plActive 1
scoreboard players set @s plTick -1
scoreboard players set @s plClip 2
scoreboard players set @s plLen 21
# heading: toward the attacker (the beat's tag), else as the avatar faces; fixed for the clip
kill @e[tag=rlk_pl_basis]
execute at @e[tag=rlk_av,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_pet","rlk_pl_basis"]}
execute at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_av,limit=1] rotated ~ 0 run tp @e[tag=rlk_pl_basis,limit=1] ~ ~ ~ ~ ~
execute if entity @e[tag=rlk_bt_atk,limit=1] as @e[tag=rlk_pl_basis,limit=1] at @s facing entity @e[tag=rlk_bt_atk,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
execute at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_pl_basis,limit=1] rotated ~ 0 run tp @e[tag=rlk_pl] ~ ~ ~ ~ 0
function rlk:char/motion/lite/hide
