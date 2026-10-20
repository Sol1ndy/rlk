# The transition message: kit banner (the element named: transition 1 the leg element, 2 the tail element) +
# the chime; the sub-line shows the message while #azTr >= 1.
execute if score #azTrN mb matches 1 if score #azLeg mb matches 1 run function rlk:mboss/azhdaha/fx/hud/banner_tr/1
execute if score #azTrN mb matches 1 if score #azLeg mb matches 2 run function rlk:mboss/azhdaha/fx/hud/banner_tr/2
execute if score #azTrN mb matches 2 if score #azTail mb matches 3 run function rlk:mboss/azhdaha/fx/hud/banner_tr/3
execute if score #azTrN mb matches 2 if score #azTail mb matches 4 run function rlk:mboss/azhdaha/fx/hud/banner_tr/4
function rlk:mboss/azhdaha/fx/snd/msg_chime
execute as @a[tag=player] at @s run playsound minecraft:block.bell.resonate hostile @s ~ ~ ~ 0.8 0.6 0.27
execute as @a[tag=player] at @s run playsound minecraft:block.respawn_anchor.charge hostile @s ~ ~ ~ 0.7 0.5 0.23
scoreboard players set #azHudQ mb 1
