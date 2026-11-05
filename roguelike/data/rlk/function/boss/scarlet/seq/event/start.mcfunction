# The event coda (PLAN §7.3.2): item 「검을 건네다」 (the thrown sword) / buff 「월하대작」 (the moonlight orb), the leave, the grant at E56, the black at E110.
# Start (@s = the body, at it; #sq hr = 0).
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_stage"]}
execute as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] at @s rotated as @e[tag=rlk_body,limit=1] run tp @s ~ ~ ~ ~ 0
scoreboard players set #sqdone hr 0
scoreboard players set @a[tag=player] hudHold 2
function rlk:boss/scarlet/rig/face/player
execute if score #hrEv hr matches 1 run function rlk:boss/scarlet/rig/play/ev_give
execute if score #hrEv hr matches 1 run function rlk:boss/scarlet/fx/snd/ev_lift
execute unless score #hrEv hr matches 1 run function rlk:boss/scarlet/rig/play/ev_toast
execute if score #hrEv hr matches 2 run function rlk:boss/scarlet/fx/snd/ev_chime
