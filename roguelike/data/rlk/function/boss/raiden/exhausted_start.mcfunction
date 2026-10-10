function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/judgment_rig/cleanup
function rlk:boss/raiden/illusion/cleanup
function rlk:boss/raiden/movement/cleanup
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
attribute @s minecraft:scale base set 1.2
kill @e[tag=rlk_rd_hazard]
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
scoreboard players set @s rdPhase 3
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdAnim 23
scoreboard players set @s rdShield 0
scoreboard players operation @a[tag=player,limit=1] energy = #burstCost100 tmp
bossbar set rlk:narukami_state color green
title @a[tag=player] times 5 45 15
title @a[tag=player] subtitle {text:"갑주 파괴 · 지금 공격하세요!",color:"green",bold:true}
playsound minecraft:entity.iron_golem.death hostile @a[tag=player] ~ ~ ~ 0.8 0.72 0.3
execute at @s run function rlk:boss/raiden/vfx/armor_break
