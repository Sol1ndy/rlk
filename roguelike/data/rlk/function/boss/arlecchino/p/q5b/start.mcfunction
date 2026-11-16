# Q5B 붉은 피의 연회 · 붉은 피의 사형 (S4, p2.py): pattern start (@s = the body, at it; #pt kn 0). Stages:
# main (q5b).
scoreboard players set #done kn 0
scoreboard players set #q5b_s kn 0
scoreboard players set #q5b_c kn 0
kill @e[type=minecraft:marker,tag=rlk_kn_q5c]
execute at @s positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q5b","rlk_kn_q5c"]}
function rlk:boss/arlecchino/p/q5b/s/main/go
