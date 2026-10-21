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
kill @e[tag=rlk_rd_hazard]
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
kill @e[tag=rlk_rd_slam_hand]
kill @e[tag=rlk_rd_sfx]
function rlk:boss/raiden/object_vfx/clear
function rlk:boss/raiden/hazard/vfx_world
scoreboard players set @e[tag=rlk_raiden] rdPat 0
scoreboard players set @e[tag=rlk_raiden] rdTime 0
scoreboard players set @e[tag=rlk_raiden] rdCool 60
scoreboard players set @e[tag=rlk_raiden] rdAnim 0
kill @e[tag=rlk_rd_tmp]
function rlk:boss/raiden/hazard/clear
execute as @e[tag=rlk_raiden,scores={rdPhase=2,rdDeath=0}] at @s run function rlk:boss/raiden/tm/idle
