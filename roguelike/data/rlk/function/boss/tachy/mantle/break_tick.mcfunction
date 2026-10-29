# G2 break + stun (#pat 52): clip, then the stun clip from 40; the transition at 160.
scoreboard players add #pt tk 1
execute if score #pt tk matches 40 run function rlk:boss/tachy/rig_stub/play/stun
execute if score #pt tk matches 40 run scoreboard players set #stun tk 120
execute if score #pt tk matches 40 run scoreboard players set #taken tk 150
execute if score #stun tk matches 1.. run scoreboard players remove #stun tk 1
execute if score #pt tk matches 160.. run function rlk:boss/tachy/mantle/end
