# A9 pattern tick 24
execute store result storage rlk:hr core.sw.d double 0.375 run scoreboard players get #sw_n hr
function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_m28,limit=1] ~ ~2.979 ~
function rlk:boss/scarlet/fx/hud/ovl {g:"magenta",in:0,hold:3,out:6}
execute at @s run function rlk:boss/scarlet/fx/snd/a9_flash
