# Q2 wheel event (@s = the prop; #pjEv 1 wall, 2 range over: it bursts here; 4 hit the player: flies on).
execute unless score #pjEv mb matches 1..2 run return 0
execute at @s run function rlk:boss/arlecchino/p/q2/burst
