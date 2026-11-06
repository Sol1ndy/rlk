# sweep clock 21
# the eruption: the 180 degree flame fan (kit flame_fan) with its roar
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p13p,limit=1] run function rlk:mboss/butterfly/fx/p/flame_fan
function rlk:mboss/butterfly/fx/snd/flame_fan
playsound minecraft:entity.ghast.shoot hostile @a[tag=player] ~ ~ ~ 0.5 1.2 0.17
