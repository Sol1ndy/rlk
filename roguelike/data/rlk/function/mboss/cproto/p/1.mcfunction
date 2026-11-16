# 1: slam at the lockv lead point (lead 10 t), a 3.5 b disc.
execute if score #cpT mb matches 1 run function rlk:mboss/mv/lockv {lead:10}
execute if score #cpT mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_lock,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:35,tell:24,dmg:120}
execute if score #cpT mb matches 1 run function rlk:mboss/cproto/rig/play {c:2}
execute if score #cpT mb matches 40.. run scoreboard players set #cpPat mb 0
