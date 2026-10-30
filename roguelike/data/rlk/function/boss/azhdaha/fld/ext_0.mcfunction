# @s = the hazard of slot 0; #azX = the requested ticks. New end = min(end + n, start + 2 x base).
scoreboard players operation #azY mb = #azFT0 mb
scoreboard players operation #azY mb += #azFB0 mb
scoreboard players operation #azY mb += #azFB0 mb
scoreboard players operation #azZ mb = #azFE0 mb
scoreboard players operation #azZ mb += #azX mb
execute if score #azZ mb > #azY mb run scoreboard players operation #azZ mb = #azY mb
scoreboard players operation #azX mb = #azZ mb
scoreboard players operation #azX mb -= #azFE0 mb
execute if score #azX mb matches ..0 run return 0
scoreboard players operation #azFE0 mb = #azZ mb
execute store result storage rlk:mboss az.ext.n int 1 run scoreboard players get #azX mb
function rlk:boss/azhdaha/fld/ext_m with storage rlk:mboss az.ext
function rlk:boss/azhdaha/fld/draw_0
