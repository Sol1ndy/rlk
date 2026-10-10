# The first lethal hit already awarded loot. Keep the brain alive only for the visual.
execute if score @s rdDeath matches 1 run return 0
scoreboard players set @s rdDeath 1
scoreboard players set @s rdDeathTime 0
scoreboard players set @s mhpC 0
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdAnim 19
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/judgment_rig/cleanup
function rlk:boss/raiden/illusion/cleanup
function rlk:boss/raiden/movement/cleanup
function rlk:boss/raiden/object/clear
function rlk:boss/raiden/object_vfx/clear
kill @e[tag=rlk_rd_hazard]
kill @e[tag=rlk_rd_dome]
kill @e[tag=rlk_rd_sfx]
kill @e[tag=rlk_rd_slam_hand]
function rlk:boss/raiden/hazard/vfx_world
execute on passengers run kill @s
# The fight is won: both boss bars disappear now, not after the collapse.
bossbar set rlk:narukami value 0
function rlk:boss/raiden/bars_hide
playsound minecraft:entity.iron_golem.death hostile @a[tag=player] ~ ~ ~ .7 .7 .3
function rlk:boss/raiden/rig/tick
