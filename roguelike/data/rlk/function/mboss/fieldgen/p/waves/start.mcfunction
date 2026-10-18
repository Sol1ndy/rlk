# 「인력 충격파」 x3 (service 21, clip wave; @s = body at the centre): impacts (24, 92, 175) (charges (24, 24, 40)),
# the 3rd wave x3 below 50 % HP; end 232.
data modify storage rlk:mboss fg.wv set value {k:5,col:"[0.98f,0.66f,0.28f]",sc:"1.8"}
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p21f]
scoreboard players set #hzAct mb 36
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 211
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzY1 mb 7
function rlk:mboss/hz/ring {r0:0,r:25,tell:24,dmg:120}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p21f
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.9 0.7 0.3
playsound minecraft:entity.breeze.charge hostile @a[tag=player] ~ ~ ~ 0.8 0.5 0.27
function rlk:mboss/fieldgen/p/waves/charge
playsound minecraft:block.respawn_anchor.ambient hostile @a[tag=player] ~ ~ ~ 0.9 1.4 0.3
