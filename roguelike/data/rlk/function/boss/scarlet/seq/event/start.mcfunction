# The event coda (PLAN §7.3.2): item 「검을 건네다」 (the thrown sword) / buff 「월하대작」 (the moonlight orb), the leave, the grant at E56, the black at E110; under the ending's lock until E118.
# Start (@s = the body, at it; #sq hr = 0).
execute unless entity @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] run function rlk:boss/scarlet/seq/event/m/alone
function rlk:mboss/mv/stop
execute unless score #sq_cx hr matches 1 as @a[tag=player,limit=1] unless entity @s[tag=rlk_body] unless entity @e[type=minecraft:marker,tag=rlk_cine_root,limit=1] at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run function rlk:char/cine/spawn
execute unless score #sq_cx hr matches 1 run function rlk:char/cine/play {clip:"coda"}
scoreboard players set #sqdone hr 0
scoreboard players set @a[tag=player] hudHold 2
title @a[tag=player] actionbar ""
execute unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/event/lock
execute facing entity @e[tag=rlk_body,limit=1] feet run rotate @s ~ 0
execute if score #hrEv hr matches 1 run function rlk:boss/scarlet/rig/play/ev_give
execute if score #hrEv hr matches 1 run function rlk:boss/scarlet/fx/snd/ev_lift
execute unless score #hrEv hr matches 1 run function rlk:boss/scarlet/rig/play/ev_toast
execute if score #hrEv hr matches 2 run function rlk:boss/scarlet/fx/snd/ev_chime
