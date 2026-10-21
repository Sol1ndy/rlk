# Armour broken (shield 0): 300 t of collapse, damage x2 (incoming), energy refilled; ends in normal_return.
function rlk:boss/raiden/illusion/cleanup
function rlk:boss/raiden/movement/cleanup
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
scoreboard players set @s rdGo 0
kill @e[tag=rlk_rd_tmp]
function rlk:boss/raiden/hazard/clear
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
kill @e[tag=rlk_rd_clap]
kill @e[tag=rlk_rd_shadow]
attribute @s minecraft:scale base set 1.2
scoreboard players set @s rdPhase 3
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdShield 0
scoreboard players operation @a[tag=player,limit=1] energy = #burstCost100 tmp
title @a[tag=player] times 5 45 15
title @a[tag=player] subtitle {text:"갑주 파괴",color:"green",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
scoreboard players set @a[tag=player] ttlT 65
scoreboard players set #rdCap rd 1
playsound minecraft:entity.iron_golem.death hostile @a[tag=player] ~ ~ ~ 0.8 0.72 0.3
execute at @s run function rlk:boss/raiden/vfx/armor_break
scoreboard players operation @s rdRigL = @s rdAnim
function rlk:boss/raiden/rig/start/t_collapse
