# 선혈의 충격 outside a window (@s = body): the crimson burst + true 2 % of the pool (clamped).
scoreboard players set #t3 kn 20
execute at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.6 1 0.6 0 40 force @a[tag=player]
execute at @s positioned ~ ~1.4 ~ run particle minecraft:explosion ~ ~ ~ 0.2 0.3 0.2 0 1 force @a[tag=player]
execute at @s run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.23
execute at @s run playsound minecraft:block.respawn_anchor.deplete hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
function rlk:boss/arlecchino/bond/true
