# The ending (hr_design §3.5): she rises, the clash, the aerial duel, the landing, the sheathe, lines 17-23, the hat tip; H at its end; locked from tick 0 into the coda.
# Cancel (no executor; idempotent): what this sequence made.
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
kill @e[type=minecraft:marker,tag=rlk_hr_stage2]
kill @e[type=minecraft:marker,tag=rlk_hr_sqh]
function rlk:mboss/cam/kill
function rlk:char/cine/stop
scoreboard players set #sq_cx hr 0
scoreboard players set #sq_h hr 0
scoreboard players set #mbCam mb 0
function rlk:boss/scarlet/fx/hud/clear
data modify storage rlk:mboss camtx.line set value {text:"",background:0}
function rlk:mboss/cam/text
data modify storage rlk:mboss camtx.hint set value {text:"",background:0}
function rlk:mboss/cam/text
scoreboard players set @a[tag=player] hudHold 0
kill @e[type=minecraft:item_display,tag=rlk_hr_sqp]
execute if data storage rlk:mboss {look_hr_field:"moon"} as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p1"}
execute if data storage rlk:mboss {look_hr_field:"crimson"} as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p2"}
