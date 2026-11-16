# The pattern set #done (@s = body): the lock marker gone, on the floor; the gauge + 3 (not A6, not U); rings at a full
# gauge -> ult at once, unless a floor step is reserved (#fl: HA-01, the step starts at the next decision, no ult);
# mx may repeat once at <= 30 % HP; after A6 the decision at once with the far rule; else the recovery.
scoreboard players set #done hr 0
scoreboard players operation #dec hr = #pat hr
scoreboard players set #pat hr 0
scoreboard players set #pt hr 0
scoreboard players set #ppf hr 0
kill @e[type=minecraft:marker,tag=rlk_hr_lock]
function rlk:boss/scarlet/core/ground
kill @e[type=minecraft:item_display,tag=rlk_hr_tr]
kill @e[type=minecraft:marker,tag=rlk_hr_trt]
execute unless score #dec hr matches 5 unless score #dec hr matches 12 run function rlk:boss/scarlet/core/gauge/pat
execute if score #dec hr matches 11 if score #ultq hr matches 1 unless score #fl hr matches 1.. run return run function rlk:boss/scarlet/core/start/ult
scoreboard players set #ultq hr 0
execute if score #dec hr matches 16 if function rlk:boss/scarlet/core/mx_rep run return 1
execute if score #dec hr matches 5 run scoreboard players set #ai_ff hr 1
execute if score #dec hr matches 5 run return run function rlk:boss/scarlet/ai/decide
function rlk:boss/scarlet/ai/rec_start
