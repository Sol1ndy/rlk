# B1 wheel event (@s = the prop; #pjEv 1 wall, 2 life over, 4 hit the player: it flies on, harmless).
execute unless score #pjEv mb matches 1..2 run return 0
execute if entity @s[tag=rlk_kn_out] run return run function rlk:boss/arlecchino/p/b1/turn
execute at @s run function rlk:boss/arlecchino/p/b1/caught
