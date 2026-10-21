# World (no @s): the player died, a run death is pending or the level-up screen is open. Runs every such tick.
function rlk:boss/raiden/camera/release_all
kill @e[tag=rlk_rd_clap]
kill @e[tag=rlk_rd_shadow]
function rlk:boss/raiden/caption/clear
function rlk:boss/raiden/judgment_rig/cleanup
function rlk:boss/raiden/illusion/cleanup
function rlk:boss/raiden/movement/cleanup
scoreboard players set @e[tag=rlk_raiden] rdBlink 0
scoreboard players set @e[tag=rlk_raiden] rdWalk 0
scoreboard players set @e[tag=rlk_raiden] rdGo 0
# Kit: every hazard and kit display (cue cards, decals); every pattern-scoped entity of both stages; rig props.
function rlk:boss/raiden/hazard/clear
kill @e[tag=rlk_rd_tmp]
function rlk:boss/raiden/rig/prop/clear
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
kill @e[tag=rlk_rd_slam_hand]
kill @e[tag=rlk_rd_sfx]
function rlk:boss/raiden/object_vfx/clear
function rlk:boss/raiden/hazard/vfx_world
execute as @e[tag=rlk_raiden,scores={rdDeath=0}] run function rlk:boss/raiden/sg/pause
scoreboard players set @e[tag=rlk_raiden] rdPat 0
scoreboard players set @e[tag=rlk_raiden] rdTime 0
scoreboard players set @e[tag=rlk_raiden] rdCool 60
scoreboard players set @e[tag=rlk_raiden] rdAnim 0
kill @e[tag=rlk_rd_tmp]
function rlk:boss/raiden/hazard/clear
execute as @e[tag=rlk_raiden,scores={rdPhase=2,rdDeath=0}] at @s run function rlk:boss/raiden/tm/idle
