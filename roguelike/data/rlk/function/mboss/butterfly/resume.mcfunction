# Hook resume (the fight runs again; module timers live in the body tick and simply continue). The pause hook
# cleared the kit's ground decals of the frozen hazards: every quiet hazard still in its tell gets its decal
# back with the tell it has left, so no strike lands without a telegraph (review fix FX-1); the running
# pattern redraws what is not a framework hazard (its optional p/<key>/resume, e.g. B2's landing markers).
execute as @e[type=minecraft:marker,tag=rlk_mb_hz,tag=rlk_mb_hzq] if score @s mbHzT < @s mbHzW at @s rotated as @s run function rlk:mboss/butterfly/u/redraw
function rlk:mboss/butterfly/p/resume_d
