# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# @s = the new basic aux husk, at it: tags, kind, state 0 (emerging, untargetable), its id, facing the Heart, the
# models riding it (om/<kind>/spawn plays the spawn clip with the 4 t scale-in).
tag @s add rlk_mb_ap_org
tag @s add rlk_mb_ap_basic
tag @s add rlk_mb_inv
scoreboard players set @s apK 1
scoreboard players set @s apS 0
scoreboard players set @s apT 0
scoreboard players set @s apShd 0
scoreboard players set @s apTok 0
scoreboard players set @s apL 0
scoreboard players set @s apSock -1
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
# melee / ranged: #apOArg 0 / 1 (wave 1: 2 + 2), otherwise 50 / 50
scoreboard players operation #apX mb = #apOArg mb
execute unless score #apX mb matches 0..1 store result score #apX mb run random value 0..1
execute if score #apX mb matches 1 run tag @s add rlk_mb_ap_rng
function rlk:boss/apep/om/basic/spawn
scoreboard players set #apOArg mb -1
scoreboard players set #apHudQ mb 1
