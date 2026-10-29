# G1: the blade element is 번개 (@s = body). Her own aura aThunder = 1U, the other one 0 (a score
# write: no damage event, so her own change never reacts); the blade edge / visor looks, the badge.
scoreboard players set #el tk 3
scoreboard players set #swt tk 0
scoreboard players set #aut tk 0
scoreboard players set @s aThunder 1000
scoreboard players set @s aFire 0
scoreboard players set @s elAct 1
function rlk:boss/tachy/el/edge
function rlk:boss/tachy/el/visor
execute unless entity @s[tag=rlk_tk_mantle] run function rlk:boss/tachy/el/badge
