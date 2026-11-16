# Q4 stage land: tick 0 (@s = body), clip q4_land.
scoreboard players set #q4_s kn 3
scoreboard players set #q4_c kn 0
function rlk:boss/arlecchino/rig/play/q4_land
execute at @s positioned ~ 201 ~ if function rlk:mboss/mv/ok run function rlk:mboss/mv/glide {t:12}
execute at @s positioned ~ 201 ~ unless function rlk:mboss/mv/ok run function rlk:boss/arlecchino/core/ground
