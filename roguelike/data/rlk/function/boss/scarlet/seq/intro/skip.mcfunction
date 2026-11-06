# The intro skip (@s = the body; PLAN §3.1): the black falls; under it the intro is cleared (line, the wind, the rock and the
# props, a walk leg in progress), she stands <= 7 b from the player facing them; the core then sets #sq to 553 and the next
# tick plays intro_end from its tick 0 (E10's end pose) with line 11 typed on the black.
function rlk:boss/scarlet/fx/hud/clear
function rlk:boss/scarlet/fx/hud/ovl {g:"black",in:0,hold:20,out:6}
stopsound @a[tag=player] * minecraft:item.elytra.flying
execute if data storage rlk:mboss {look_hr_field:"moon"} as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p1"}
execute if data storage rlk:mboss {look_hr_field:"crimson"} as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p2"}
scoreboard players set @a[tag=player] hudHold 2
function rlk:mboss/mv/stop
execute positioned 884.0 201 5.0 run kill @e[type=minecraft:item_display,tag=rlk_hr_deco,distance=..1]
function rlk:boss/scarlet/rig/look/props/none
function rlk:mboss/mv/dist
function rlk:boss/scarlet/seq/intro/m/near7
function rlk:boss/scarlet/rig/face/player
