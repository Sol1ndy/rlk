# One heal orb here (the existing combat/heal_orb_spawn), tagged as hers.
function rlk:combat/heal_orb_spawn
tag @e[type=minecraft:item,tag=rlk_healorb,tag=!rlk_kn_orb,distance=..2] add rlk_mb_aux
tag @e[type=minecraft:item,tag=rlk_healorb,tag=!rlk_kn_orb,distance=..2] add rlk_room
tag @e[type=minecraft:item,tag=rlk_healorb,tag=!rlk_kn_orb,distance=..2] add rlk_kn_orb
function rlk:boss/arlecchino/fx/snd/orb_spawn
