# A reload cancels pending danger volumes; it never refills boss health (the weapon and the switch after-effect stay).
execute if score @s rdDeath matches 1 run return run kill @s
scoreboard players set @s rdDeath 0
scoreboard players set @s rdDeathTime 0
scoreboard players set @s rdUltUsed 0
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
scoreboard players set @s rdHidden 0
tag @s remove rlk_rd_armoured
kill @e[tag=rlk_rd_blink_dest]
function rlk:boss/raiden/illusion/cleanup
attribute @s minecraft:scale base set 1.2
# A reload in the Tenma / exhausted phases returns her to the Shogun phase: give the arena its Shogun floor back too.
execute if score @s rdPhase matches 1.. if entity @e[tag=rlk_raiden_arena,limit=1] run function rlk:room/raiden/look_shogun
scoreboard players set @s rdPhase 0
scoreboard players set @s rdPat 0
scoreboard players set @s rdGo 0
scoreboard players set @s rdNext 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdRage 0
scoreboard players set @s rdCool 40
scoreboard players set @s rdHitCD 0
function rlk:boss/raiden/sg/reload
function rlk:boss/raiden/rig/spawn
function rlk:boss/raiden/sg/look
