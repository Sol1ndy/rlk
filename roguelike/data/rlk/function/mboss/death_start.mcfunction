# @s = body whose HP reached 0 in combat/apply (heal orb, XP and gold of the lethal hit already paid).
# The body keeps rlk_zmob until death_finish, so the zone clears only after the death sequence.
execute if entity @s[tag=rlk_mb_dying] run return 0
tag @s add rlk_mb_dying
tag @s add rlk_mb_inv
scoreboard players set @s mhpC 0
scoreboard players set #mbKilled mb 1
scoreboard players set #mbSt mb 2
scoreboard players set #mbT mb 0
function rlk:mboss/lib_clear
function rlk:mboss/bars_hide
# Generic death roar unless the registry entry sets deathSnd false (the module plays its own death sound).
execute unless data storage rlk:mboss cur{deathSnd:0b} at @s run playsound minecraft:entity.wither.death hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
# chapter mode (AZ-CM): proxies to the dead set (inv: nothing targetable), the music stops (a sting is the module's)
execute if score #mbPx mb matches 1 run function rlk:mboss/px/state {set:"dead"}
function rlk:mboss/music/stop
function rlk:mboss/d/death_start
