# repel {at:60|5} (hr_design §3.4): the deflect, the blade lock, the grab, the hilt on her hat, two cuts, back to back, the throw, the kick; HP steps at 49 / 101 / 129; locked 0-140, the bars on.
# Cancel (no executor; idempotent): what this sequence made.
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
kill @e[type=minecraft:marker,tag=rlk_hr_stage2]
kill @e[type=minecraft:marker,tag=rlk_hr_sqh]
function rlk:mboss/cam/kill
scoreboard players set #sq_cx hr 0
scoreboard players set #sq_h hr 0
scoreboard players set #mbNoLeash mb 0
kill @e[type=minecraft:item_display,tag=rlk_hr_sqp]
