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
execute if score #skip hr matches 0..0 run title @a[tag=player] actionbar ["",{text:"⊙ 건너뛰기",color:"#A8A8B0"},{text:" · Shift 길게",color:"#A8A8B0"}]
execute if score #skip hr matches 0..0 run scoreboard players set @a[tag=player] hudHold 2
execute if score #skip hr matches 1..5 run title @a[tag=player] actionbar ["",{text:"⊙ 건너뛰기",color:"#BDBDC4"},{text:" · Shift 길게",color:"#BDBDC4"}]
execute if score #skip hr matches 1..5 run scoreboard players set @a[tag=player] hudHold 2
execute if score #skip hr matches 6..10 run title @a[tag=player] actionbar ["",{text:"⊙ 건너뛰기",color:"#D0D0D6"},{text:" · Shift 길게",color:"#D0D0D6"}]
execute if score #skip hr matches 6..10 run scoreboard players set @a[tag=player] hudHold 2
execute if score #skip hr matches 11..15 run title @a[tag=player] actionbar ["",{text:"⊙ 건너뛰기",color:"#E4E4E8"},{text:" · Shift 길게",color:"#E4E4E8"}]
execute if score #skip hr matches 11..15 run scoreboard players set @a[tag=player] hudHold 2
execute if score #skip hr matches 16..19 run title @a[tag=player] actionbar ["",{text:"⊙ 건너뛰기",color:"#FFFFFF"},{text:" · Shift 길게",color:"#FFFFFF"}]
execute if score #skip hr matches 16..19 run scoreboard players set @a[tag=player] hudHold 2
