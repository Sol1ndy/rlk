# @s = the hazard of slot 2; #azX = the requested ticks. New end = min(end + n, start + 2 x base).
scoreboard players operation #azY mb = #azFT2 mb
scoreboard players operation #azY mb += #azFB2 mb
scoreboard players operation #azY mb += #azFB2 mb
scoreboard players operation #azZ mb = #azFE2 mb
scoreboard players operation #azZ mb += #azX mb
execute if score #azZ mb > #azY mb run scoreboard players operation #azZ mb = #azY mb
scoreboard players operation #azX mb = #azZ mb
scoreboard players operation #azX mb -= #azFE2 mb
execute if score #azX mb matches ..0 run return 0
scoreboard players operation #azFE2 mb = #azZ mb
execute store result storage rlk:mboss az.ext.n int 1 run scoreboard players get #azX mb
function rlk:boss/azhdaha/fld/ext_m with storage rlk:mboss az.ext
function rlk:boss/azhdaha/fld/draw_2
