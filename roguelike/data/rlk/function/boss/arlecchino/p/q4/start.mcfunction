# Q4 떠오르는 재액의 달 (S4, p2.py): pattern start (@s = the body, at it; #pt kn 0). Stages:
# up (q4_up) -> shot (q4_shot) -> land (q4_land).
scoreboard players set #done kn 0
scoreboard players set #q4_s kn 0
scoreboard players set #q4_c kn 0
scoreboard players set #q4_n kn 1
scoreboard players set #q4_k kn 0
execute store result score #t kn run scoreboard players get @s mhpC
scoreboard players operation #t kn *= #c100 kn
execute store result score #t2 kn run scoreboard players get @s mhpM
scoreboard players set #t3 kn 50
scoreboard players operation #t2 kn *= #t3 kn
execute if score #t kn <= #t2 kn run scoreboard players set #q4_n kn 3
execute if score #tst kn matches 45 run scoreboard players set #q4_n kn 3
execute if score #tst kn matches 45 run scoreboard players set #tst kn 0
execute if score #mbLock mb matches 45 run scoreboard players set #q4_n kn 3
function rlk:boss/arlecchino/p/q4/s/up/go
