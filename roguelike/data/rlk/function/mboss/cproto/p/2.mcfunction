# 2: the push ring around the body (within 6 b -> out to 6.5 b over 4 t), after a short tell.
execute if score #cpT mb matches 1 at @s positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:60,tell:16,dmg:0}
execute if score #cpT mb matches 16 at @s run function rlk:mboss/push/ring {r:60,to:65,kb:4}
execute if score #cpT mb matches 40.. run scoreboard players set #cpPat mb 0
