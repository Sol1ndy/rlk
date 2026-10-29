# /reload during the mantle (@s = body; the rig and every marker are new): the gauge and the time are kept, the
# clip comes back; a break / stun goes on; a running nova (its markers are gone) ends: the transition.
execute if score #pat tk matches 51 run function rlk:boss/tachy/rig/play/mantle_hold
execute if score #pat tk matches 51 run scoreboard players set #hud_g tk -1
execute if score #pat tk matches 51 run scoreboard players set #hud_c tk -1
execute if score #pat tk matches 51 run function rlk:boss/tachy/mantle/badge9
execute if score #pat tk matches 52 if score #pt tk matches 40.. run function rlk:boss/tachy/rig/play/stun
execute if score #pat tk matches 52 if score #pt tk matches ..39 run function rlk:boss/tachy/rig/play/mantle_break
execute if score #pat tk matches 53 run function rlk:boss/tachy/mantle/end
