# Q6 stage main tick 30
execute if entity @e[tag=rlk_kn_moon,limit=1] at @e[tag=rlk_kn_moon,limit=1] run function rlk:boss/arlecchino/fx/p/moon_flare
execute unless entity @e[tag=rlk_kn_moon,limit=1] at @s run function rlk:boss/arlecchino/fx/p/moon_flare
execute at @s run function rlk:boss/arlecchino/fx/snd/moon
