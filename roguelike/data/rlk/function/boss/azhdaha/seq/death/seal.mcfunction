# The seal re-forms around the body (the gold glyph prism again, UUID 0x80) and the rig petrifies.
function rlk:boss/azhdaha/rig/look/petrify
function rlk:boss/azhdaha/fx/p/seal_reform
function rlk:boss/azhdaha/fx/snd/death_seal
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
execute at @s positioned ~ 201 ~ run kill @e[type=minecraft:item_display,tag=rlk_mb_az_seal_prism]
execute at @s positioned ~ 201 ~ run summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,128],Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_seal","rlk_mb_az_seal_prism"],billboard:"fixed",brightness:{block:15,sky:15},item:{id:"minecraft:yellow_stained_glass",count:1}}
execute at @s positioned ~ 201 ~ run execute as @e[type=minecraft:item_display,tag=rlk_mb_az_seal_prism] run function rlk:boss/azhdaha/fx/prop/seal_prism
