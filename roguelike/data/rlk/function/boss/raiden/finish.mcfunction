# As the boss: the pattern is over. Non-detached hazards go (kit hazard/finish), pattern props go.
function rlk:boss/raiden/camera/release_all
kill @e[tag=rlk_rd_clap]
kill @e[tag=rlk_rd_shadow]
function rlk:boss/raiden/caption/pattern_end
function rlk:boss/raiden/judgment_rig/cleanup
function rlk:boss/raiden/hazard/finish
kill @e[tag=rlk_rd_sg]
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
scoreboard players set @s rdGo 0
kill @e[tag=rlk_rd_blink_dest]
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdAnim 0
scoreboard players set @s rdCool 16
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
execute if score @s rdPhase matches 0 run function rlk:boss/raiden/sg/finish
kill @e[tag=rlk_rd_tm]
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/tm/after
