# CS0 intro (hr_design §3.1): 20 shots, lines 1-11; seated with the cup and the bottle, the walk, the leap; intro_end: line 11, the draw, the stance.
# Cancel (no executor; idempotent): what this sequence made.
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
kill @e[type=minecraft:marker,tag=rlk_hr_stage2]
kill @e[type=minecraft:marker,tag=rlk_hr_sqh]
function rlk:mboss/cam/kill
scoreboard players set #sq_cx hr 0
scoreboard players set #sq_h hr 0
stopsound @a[tag=player] * minecraft:item.elytra.flying
kill @e[type=minecraft:item_display,tag=rlk_hr_sqp]
execute if data storage rlk:mboss {look_hr_field:"moon"} as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p1"}
execute if data storage rlk:mboss {look_hr_field:"crimson"} as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p2"}
