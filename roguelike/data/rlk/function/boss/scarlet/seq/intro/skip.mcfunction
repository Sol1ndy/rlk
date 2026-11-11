# The intro skip (@s = the body; hr_design §3.1): the black falls; under it the intro is cleared (the line, the wind, the
# rock and the props, a move in progress, the petal), she stands at f 6.5 facing the actor (the landing's place), camera B
# is put where I18 wants it; the core then sets #sq to 1289 and the next tick plays intro_end from its tick 0 (line 11
# typed on the black). The actor shows its tick 1290 by itself (#cavT cine follows #sq).
function rlk:boss/scarlet/fx/hud/clear
function rlk:boss/scarlet/fx/hud/ovl {g:"black",in:0,hold:20,out:6}
stopsound @a[tag=player] * minecraft:item.elytra.flying
execute if data storage rlk:mboss {look_hr_field:"moon"} as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p1"}
execute if data storage rlk:mboss {look_hr_field:"crimson"} as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p2"}
scoreboard players set @a[tag=player] hudHold 2
kill @e[type=minecraft:item_display,tag=rlk_hr_sqp]
function rlk:mboss/mv/stop
execute positioned 884.0 201 5.0 run kill @e[type=minecraft:item_display,tag=rlk_hr_deco,distance=..1]
function rlk:boss/scarlet/rig/look/props/none
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^0 ^6.5 run tp @s ~ ~ ~
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @s ~180 0
execute unless score #sq_cx hr matches 1 run function rlk:mboss/cam/spawn
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] ^-0.15 ^1.35 ^1 facing ^0 ^1.62 ^0
