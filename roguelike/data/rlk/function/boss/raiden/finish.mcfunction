function rlk:boss/raiden/camera/release_all
kill @e[tag=rlk_rd_clap]
kill @e[tag=rlk_rd_shadow]
function rlk:boss/raiden/caption/pattern_end
function rlk:boss/raiden/judgment_rig/cleanup
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
scoreboard players set @s rdGo 0
kill @e[tag=rlk_rd_blink_dest]
scoreboard players operation #rdWalkTurn rd = @s rdTurns
scoreboard players set #rd2 rd 2
scoreboard players operation #rdWalkTurn rd %= #rd2 rd
execute if score #rdWalkTurn rd matches 0 run function rlk:boss/raiden/movement/walk_start
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdAnim 0
scoreboard players set @s rdCool 10
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
kill @e[tag=rlk_rd_tm]
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/tm/after
