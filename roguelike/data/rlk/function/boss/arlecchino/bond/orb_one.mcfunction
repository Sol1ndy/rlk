# One heal orb here (the existing combat/heal_orb_spawn), tagged as hers.
function rlk:combat/heal_orb_spawn
tag @e[type=minecraft:item,tag=rlk_healorb,tag=!rlk_kn_orb,distance=..2] add rlk_mb_aux
tag @e[type=minecraft:item,tag=rlk_healorb,tag=!rlk_kn_orb,distance=..2] add rlk_room
tag @e[type=minecraft:item,tag=rlk_healorb,tag=!rlk_kn_orb,distance=..2] add rlk_kn_orb
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
