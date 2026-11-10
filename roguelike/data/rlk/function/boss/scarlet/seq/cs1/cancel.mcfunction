# CS1 (hr_design §3.2): the clash, pushed apart, the hat and the bottle, the petal, 홍련일섬, the crimson field; locked 0-720, skippable 40-560 -> 566.
# Cancel (no executor; idempotent): what this sequence made.
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
kill @e[type=minecraft:marker,tag=rlk_hr_stage2]
kill @e[type=minecraft:marker,tag=rlk_hr_sqh]
function rlk:mboss/cam/kill
scoreboard players set #sq_cx hr 0
scoreboard players set #sq_h hr 0
scoreboard players set #mbNoLeash mb 0
kill @e[type=minecraft:item_display,tag=rlk_hr_sqp]
