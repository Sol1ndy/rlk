# intro at #sq 146 (@s = the body).
function rlk:boss/scarlet/fx/hud/line {id:4}
execute if data storage rlk:mboss {look_hr_field:"moon"} as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p1"}
execute if data storage rlk:mboss {look_hr_field:"crimson"} as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p2"}
