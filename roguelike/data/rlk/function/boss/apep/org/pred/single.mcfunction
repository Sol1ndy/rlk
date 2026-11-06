# A single bite at apTok: the lunge prep from apTok - 12 (the flare + o6_swim, it dashes in to 2 b in 2 t), the sector
# locked at apTok - 10, pred_bite at apTok - 4 (snap 4), the bite at apTok. Before the prep it circles.
scoreboard players operation #apX mb = @s apTok
scoreboard players remove #apX mb 12
execute if score @s apT < #apX mb run return run function rlk:boss/apep/org/pred/orbit
execute if score @s apT = #apX mb run function rlk:boss/apep/org/pred/single_cue
scoreboard players add #apX mb 2
execute if score @s apT < #apX mb unless entity @e[tag=rlk_body,distance=..2] facing entity @e[tag=rlk_body,limit=1] feet run function rlk:mboss/mv/step_flat {spd:1.5}
function rlk:boss/apep/org/basic/push_in
execute if score @s apT = #apX mb run function rlk:boss/apep/org/pred/single_hz
scoreboard players add #apX mb 6
execute if score @s apT = #apX mb run function rlk:boss/apep/om/pred/play/pred_bite
execute if score @s apT >= @s apTok run function rlk:boss/apep/org/pred/single_hit
