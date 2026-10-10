function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/judgment_rig/cleanup
function rlk:boss/raiden/illusion/cleanup
scoreboard players set @s rdWalk 0
kill @e[tag=rlk_rd_hazard]
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
scoreboard players set @s rdPhase 1
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players add @s rdCycle 1
# Scatter to the arena centre (depart here, reform there) instead of snapping to it;
# an unfinished blink is redirected there. Relocation lands by rdTime 4 at the latest.
kill @e[tag=rlk_rd_blink_dest]
scoreboard players set #rdGo rd 0
execute if score @s rdBlink matches 1.. run scoreboard players set #rdGo rd 1
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..1.5] run scoreboard players set #rdGo rd 1
execute if score #rdGo rd matches 1 at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/movement/blink_to
scoreboard players set @s rdAnim 9
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
title @a[tag=player] times 8 55 16
title @a[tag=player] subtitle {text:"번개 갑주를 파괴하면 잠시 무력화됩니다",color:"white"}
title @a[tag=player] title {text:"악요의 요구우 텐마",color:"light_purple",bold:true}
scoreboard players set @a[tag=player] vBig 79
scoreboard players set @a[tag=player] ttlT 79
scoreboard players set #rdCap rd 1
# Not a pattern caption: an interrupted illusion caption must not let armor_start's
# finish (rdTime 56) cut this one short.
scoreboard players set #rdCapPat rd 0
playsound minecraft:entity.wither.spawn hostile @a[tag=player] ~ ~ ~ 0.8 0.5 0.4
