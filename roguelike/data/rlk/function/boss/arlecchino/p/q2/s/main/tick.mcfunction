# Q2 stage main: one tick (#q2_c 1..).
execute if score #q2_c kn matches 1..14 run function rlk:mboss/mv/turn {max:10}
execute if score #q2_c kn matches 21..31 as @e[tag=rlk_kn_p_q2,tag=rlk_kn_wheel] at @s positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1,distance=..0.8] at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run function rlk:boss/arlecchino/p/q2/burst
execute if score #q2_c kn matches 6 at @s run function rlk:boss/arlecchino/fx/snd/wheel_spin
execute if score #q2_c kn matches 14 run function rlk:boss/arlecchino/p/q2/s/main/k/14
execute if score #q2_c kn matches 20 run function rlk:boss/arlecchino/p/q2/s/main/k/20
execute if score #q2_c kn matches 33 run function rlk:boss/arlecchino/p/q2/s/main/k/33
execute if score #q2_c kn matches 34 run function rlk:boss/arlecchino/p/q2/s/main/k/34
execute if score #q2_c kn matches 40 run function rlk:boss/arlecchino/p/q2/s/main/k/40
execute if score #q2_c kn matches 41 run function rlk:boss/arlecchino/p/q2/s/main/k/41
execute if score #q2_c kn matches 42 if score #q2_sl kn matches 1 run function rlk:boss/arlecchino/p/q2/f/slash_fx
execute if score #q2_c kn matches 48 run return run function rlk:boss/arlecchino/p/q2/s/main/k/48
execute if score #q2_c kn matches 70 run return run function rlk:boss/arlecchino/p/q2/s/main/k/70
