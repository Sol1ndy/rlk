# 카이라기·뇌전 (@s = brain, at @s; cm/tick hook). A: 3 zig-zag dash slashes -> 1.2 s spent (punish).
# B: electro spin slash after a 0.8 s blade glow. Not staggerable from the first tell to the last dash / the spin.
function rlk:cm/kr/lib/pre
execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/kr/reset
execute if score @s cmS matches 1 run return run function rlk:cm/kr/a_tell
execute if score @s cmS matches 2 run return run function rlk:cm/kr/a_after
execute if score @s cmS matches 3 run return run function rlk:cm/kr/a_rest
execute if score @s cmS matches 4 run return run function rlk:cm/kr/b_tell
execute if score @s cmS matches 5 run return run function rlk:cm/kr/b_rest
execute if score #free tmp matches 0 run return 0
execute if score @s cmCd2 matches ..0 if entity @e[tag=rlk_body,distance=..3.2] run return run function rlk:cm/kr/b_start
execute if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..7.5] run function rlk:cm/kr/a_start
