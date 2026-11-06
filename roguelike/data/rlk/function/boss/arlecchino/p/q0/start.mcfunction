# Q0 낙하 공격 (S4, p2.py): pattern start (@s = the body, at it; #pt kn 0). Stages:
# hover (q0_hover) -> dive (q0_dive).
scoreboard players set #done kn 0
scoreboard players set #q0_s kn 0
scoreboard players set #q0_c kn 0
kill @e[type=minecraft:marker,tag=rlk_kn_q0p]
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q0","rlk_kn_q0p"]}
function rlk:boss/arlecchino/p/q0/s/hover/go
