# Q1 crescent event (@s = the prop; #pjEv 1 wall, 2 range over, 4 hit the player: it flies on).
execute unless score #pjEv mb matches 1..2 run return 0
execute if entity @s[tag=rlk_kn_out] run return run function rlk:boss/arlecchino/p/q1/cres_turn
execute at @s run function rlk:boss/arlecchino/fx/snd/wheel_catch
