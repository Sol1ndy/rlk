# A reload cancels pending danger volumes; it never refills boss health.
execute if score @s rdDeath matches 1 run return run kill @s
scoreboard players set @s rdDeath 0
scoreboard players set @s rdDeathTime 0
scoreboard players set @s rdUltUsed 0
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
scoreboard players set @s rdHidden 0
kill @e[tag=rlk_rd_blink_dest]
function rlk:boss/raiden/illusion/cleanup
attribute @s minecraft:scale base set 1.2
scoreboard players set @s rdPhase 0
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdRage 0
scoreboard players set @s rdCool 40
scoreboard players set @s rdAnim 0
scoreboard players set @s rdHitCD 0
function rlk:boss/raiden/rig/spawn
