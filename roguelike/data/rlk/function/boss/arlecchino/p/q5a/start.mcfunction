# Q5A 붉은 피의 연회 · 형벌의 핏값 (S4, p2.py): pattern start (@s = the body, at it; #pt kn 0). Stages:
# main (q5a).
scoreboard players set #done kn 0
scoreboard players set #q5a_s kn 0
scoreboard players set #q5a_c kn 0
kill @e[type=minecraft:marker,tag=rlk_kn_q5c]
execute at @s positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q5a","rlk_kn_q5c"]}
function rlk:boss/arlecchino/p/q5a/s/main/go
