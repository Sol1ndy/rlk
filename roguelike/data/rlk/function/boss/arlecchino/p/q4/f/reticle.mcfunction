# Q4 the reticle (@s = body, once per shot): at the chest anchor toward the player.
kill @e[type=minecraft:marker,tag=rlk_kn_q4c]
function rlk:boss/arlecchino/p/q4/f/chest
execute at @e[type=minecraft:marker,tag=rlk_kn_q4c,limit=1] facing entity @e[tag=rlk_body,limit=1] eyes run function rlk:boss/arlecchino/fx/p/reticle
