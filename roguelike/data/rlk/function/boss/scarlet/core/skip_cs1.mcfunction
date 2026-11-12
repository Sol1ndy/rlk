# The cs1 skip input (@s = body, every tick of the sequence; hr_design §3.0): from 40 to 560 the prompt
# ⊙ 건너뛰기 · Space 길게 (hudHold); holding the jump key (rlk:in_jump; round V: Shift is no input) brightens it in 4 steps of 5 t, a release
# resets the count; 20 t held -> the skip (seq/cs1/skip, then #sq = 565: the next tick is 566).
# Parked while a sequence of seq.py runs (seq/cs1/skipin holds #skip at -1 and reads the key itself): this input
# only serves a stand-in sequence.
execute if score #skip hr matches ..-1 run return 0
execute if score #skp hr matches 1.. if score #sq hr = #skp hr run return run function rlk:boss/scarlet/core/skip_cs1_go
execute if score #sq hr matches 561.. run return run function rlk:boss/scarlet/core/skip_clear
execute unless score #sq hr matches 40..560 run return 0
execute as @a[tag=player,limit=1] if predicate rlk:in_jump run scoreboard players add #skip hr 1
execute as @a[tag=player,limit=1] unless predicate rlk:in_jump run scoreboard players set #skip hr 0
execute if score #skip hr matches 20.. run return run function rlk:boss/scarlet/core/skip_cs1_go
execute if score #skip hr matches 0..0 run function rlk:boss/scarlet/fx/hud/skip {s:0}
execute if score #skip hr matches 1..5 run function rlk:boss/scarlet/fx/hud/skip {s:1}
execute if score #skip hr matches 6..10 run function rlk:boss/scarlet/fx/hud/skip {s:2}
execute if score #skip hr matches 11..15 run function rlk:boss/scarlet/fx/hud/skip {s:3}
execute if score #skip hr matches 16..19 run function rlk:boss/scarlet/fx/hud/skip {s:4}
