# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# @s = the new destr aux husk, at it: tags, kind, state 0 (emerging, untargetable), its id, facing the Heart, the
# models riding it (om/<kind>/spawn plays the spawn clip with the 4 t scale-in).
tag @s add rlk_mb_ap_org
tag @s add rlk_mb_ap_destr
tag @s add rlk_mb_inv
scoreboard players set @s apK 5
scoreboard players set @s apS 0
scoreboard players set @s apT 0
scoreboard players set @s apShd 0
scoreboard players set @s apTok 0
scoreboard players set @s apL 0
scoreboard players set @s apSock 0
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
scoreboard players add #apOrgN mb 1
scoreboard players operation @s apL = #apOrgN mb
function rlk:boss/apep/om/destr/spawn
scoreboard players set #apOArg mb -1
scoreboard players set #apHudQ mb 1
