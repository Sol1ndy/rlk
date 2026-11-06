# The intro skip input (@s = body, every intro tick; PLAN §3.1): from 20 to 540 the prompt ⊙ 건너뛰기 · Shift 길게
# (hudHold); holding sneak (rlk:in_sneak) brightens it in 4 steps of 5 t, a release resets the count;
# 20 t held -> the skip (seq/intro/skip, then #sq = 553: the next tick plays intro_end from 0).
execute if score #skip hr matches ..-1 run return 0
execute if score #skp hr matches 1.. if score #sq hr = #skp hr run return run function rlk:boss/scarlet/core/skip_go
execute if score #sq hr matches 541.. run return run function rlk:boss/scarlet/core/skip_clear
execute unless score #sq hr matches 20..540 run return 0
execute as @a[tag=player,limit=1] if predicate rlk:in_sneak run scoreboard players add #skip hr 1
execute as @a[tag=player,limit=1] unless predicate rlk:in_sneak run scoreboard players set #skip hr 0
execute if score #skip hr matches 20.. run return run function rlk:boss/scarlet/core/skip_go
execute if score #skip hr matches 0..0 run function rlk:boss/scarlet/fx/hud/skip {s:0}
execute if score #skip hr matches 1..5 run function rlk:boss/scarlet/fx/hud/skip {s:1}
execute if score #skip hr matches 6..10 run function rlk:boss/scarlet/fx/hud/skip {s:2}
execute if score #skip hr matches 11..15 run function rlk:boss/scarlet/fx/hud/skip {s:3}
execute if score #skip hr matches 16..19 run function rlk:boss/scarlet/fx/hud/skip {s:4}
