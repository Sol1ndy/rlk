# Q2 dash (@s = body, 1 t before go): facing the player, to 1.5 b in front of them (at most 20 b; core/dash/probe:
# every 0.5 b step passes mv/ok), glided over 8 t; the end marker rlk_kn_q2e decides the slash.
function rlk:mboss/mv/face
function rlk:mboss/mv/dist
scoreboard players operation #t kn = #mbDist mb
scoreboard players remove #t kn 15
scoreboard players operation #t kn /= #c5 kn
execute if score #t kn matches ..0 run scoreboard players set #t kn 0
execute if score #t kn matches 41.. run scoreboard players set #t kn 40
function rlk:boss/arlecchino/core/dash/probe
kill @e[type=minecraft:marker,tag=rlk_kn_q2e]
execute positioned as @e[type=minecraft:marker,tag=rlk_kn_dp,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q2","rlk_kn_q2e"]}
execute positioned as @e[type=minecraft:marker,tag=rlk_kn_dp,limit=1] run function rlk:mboss/mv/glide {t:8}
kill @e[type=minecraft:marker,tag=rlk_kn_dp]
