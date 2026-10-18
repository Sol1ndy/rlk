# release clock 53
# E: the detonation: white flash, the lime dome r 10 (kit rel_dome) at R, the big boom, a white screen flash
kill @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod]
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] run function rlk:mboss/butterfly/fx/p/rel_dome {r:10}
function rlk:mboss/butterfly/fx/snd/release_boom
function rlk:mboss/butterfly/fx/hud/flash_white
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] run particle minecraft:explosion_emitter ~ ~2 ~ 0 0 0 0 1 force @a[tag=player]
