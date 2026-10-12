function rlk:boss/raiden/camera/release_all
scoreboard players set @s rdGo 0
scoreboard players set @s rdNext 0
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
# Transforms where it stands (normally only after its pattern ended). A test/forced
# start can land mid-blink: let that blink finish in place without a destination.
kill @e[tag=rlk_rd_blink_dest]
scoreboard players set @s rdAnim 9
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
function rlk:boss/raiden/line/eternal
scoreboard players set #rdCapPat rd 0
playsound minecraft:entity.wither.spawn hostile @a[tag=player] ~ ~ ~ 0.8 0.5 0.4
