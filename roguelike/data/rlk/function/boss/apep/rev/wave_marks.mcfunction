# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# The spawn markers of wave #apWave (a new wave, or /reload: the current one again; plan 7.6.3): 4 basics on 4
# distinct r 12 points never closer than 4 b to the player (wave 1: 2 melee + 2 ranged, later 50 / 50), then the
# wave's specials on their points (수호 nearest 10 b from the player, 둥지 nearest the player, 포식성 farthest, 양육 on
# the r 7 point nearest the new basics); waves 2-5 the table, 6 one from the shuffle bag, 7+ two.
function rlk:boss/apep/rev/cands
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_cand,sort=random,limit=1] at @s run function rlk:boss/apep/rev/mk_basic0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_cand,sort=random,limit=1] at @s run function rlk:boss/apep/rev/mk_basic1
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_cand,sort=random,limit=1] at @s run function rlk:boss/apep/rev/mk_basic2
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_cand,sort=random,limit=1] at @s run function rlk:boss/apep/rev/mk_basic3
execute if score #apWave mb matches 2 run function rlk:boss/apep/rev/mk_guard
execute if score #apWave mb matches 3 run function rlk:boss/apep/rev/mk_nest
execute if score #apWave mb matches 4 run function rlk:boss/apep/rev/mk_nurt
execute if score #apWave mb matches 5 run function rlk:boss/apep/rev/mk_pred
execute if score #apWave mb matches 6.. run function rlk:boss/apep/rev/bag
execute if score #apWave mb matches 7.. run function rlk:boss/apep/rev/bag
kill @e[type=minecraft:marker,tag=rlk_mb_ap_cand]
