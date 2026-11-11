# lead5 (hr_design §3.3; the 5 % floor): the stagger, she backs off to 10 b, the gauge refilled (+ the banner), the glow, the hand to the brim; G2 at its end. Not locked.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 116.
execute if score #sq hr matches 116.. run scoreboard players set #sqdone hr 1
execute if score #sq hr matches 1..7 run return run function rlk:boss/scarlet/seq/lead5/k/1_7
execute if score #sq hr matches 8..59 run return run function rlk:boss/scarlet/seq/lead5/k/8_59
execute if score #sq hr matches 60 run return run function rlk:boss/scarlet/seq/lead5/k/60
execute if score #sq hr matches 61..83 run return run function rlk:boss/scarlet/seq/lead5/k/61_83
execute if score #sq hr matches 84 run return run function rlk:boss/scarlet/seq/lead5/k/84
execute if score #sq hr matches 85..97 run return run function rlk:boss/scarlet/seq/lead5/k/85_97
execute if score #sq hr matches 98 run return run function rlk:boss/scarlet/seq/lead5/k/98
execute if score #sq hr matches 99..116 run return run function rlk:boss/scarlet/seq/lead5/k/99_116
