# Every state of the fight stops (death, cleanup, tests; any executor): the pattern / gauntlet, the running
# sequence, the shield, the pattern hazards and markers, the glide.
function rlk:boss/scarlet/core/cancel_d
execute if score #sqn hr matches 1 run function rlk:boss/scarlet/core/sq/intro/cancel
execute if score #sqn hr matches 2 run function rlk:boss/scarlet/core/sq/cs1/cancel
execute if score #sqn hr matches 3 run function rlk:boss/scarlet/core/sq/lead60/cancel
execute if score #sqn hr matches 4 run function rlk:boss/scarlet/core/sq/repel/cancel
execute if score #sqn hr matches 5 run function rlk:boss/scarlet/core/sq/lead5/cancel
execute if score #sqn hr matches 6 run function rlk:boss/scarlet/core/sq/lead_re/cancel
execute if score #sqn hr matches 7 run function rlk:boss/scarlet/core/sq/ending/cancel
execute if score #sqn hr matches 8 run function rlk:boss/scarlet/core/sq/event/cancel
scoreboard players set #pat hr 0
scoreboard players set #pt hr 0
scoreboard players set #done hr 0
scoreboard players set #sqn hr 0
scoreboard players set #sqdone hr 0
scoreboard players set #sq_sig hr 0
scoreboard players set #rvw hr 0
scoreboard players set #kip hr 0
scoreboard players set #flw hr 0
scoreboard players set #grs hr 0
scoreboard players set #rp hr 0
function rlk:boss/scarlet/shield/off
kill @e[tag=rlk_hr_p]
kill @e[tag=rlk_hr_cut]
kill @e[type=minecraft:marker,tag=rlk_hr_lock]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1,tag=rlk_mb_mv] run function rlk:mboss/mv/stop
