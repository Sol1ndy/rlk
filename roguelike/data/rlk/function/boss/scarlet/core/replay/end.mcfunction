function rlk:boss/scarlet/seq/intro/cancel
function rlk:boss/scarlet/core/skip_clear
scoreboard players set #rp hr 0
scoreboard players set #sqn hr 0
scoreboard players set #sq hr 0
scoreboard players set #sqdone hr 0
scoreboard players set #skp hr 0
kill @e[tag=rlk_hr_deco_seat_rock]
execute if score #ph hr matches 1 run scoreboard players set #inv hr 0
execute if score #ph hr matches 7 run scoreboard players set #inv hr 0
function rlk:boss/scarlet/core/looks
function rlk:boss/scarlet/ai/rec_start
