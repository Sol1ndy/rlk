# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# Macro {k,a}: a pending spawn of kind apK k (a = the basic's melee 0 / ranged 1, -1 random) at the execution
# point: the kit spawn marker (pale wireframe dome) for 20 t, then the organism (org/pend).
execute positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_ospawn","rlk_mb_ap_new"]}
$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_new] apK $(k)
$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_new] apS $(a)
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_new] apT 0
tag @e[type=minecraft:marker,tag=rlk_mb_ap_new] remove rlk_mb_ap_new
execute positioned ~ 201 ~ run function rlk:boss/apep/fx/p/spawn_marker
execute positioned ~ 201 ~ run function rlk:boss/apep/fx/snd/spawn_marker
