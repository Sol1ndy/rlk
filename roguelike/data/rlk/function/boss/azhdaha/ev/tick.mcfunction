# @s = body: the floor events (plan 4.3): a hit with mhpC - raw <= #mbFloor (#mbFloorHit, framework) or mhpC <=
# #mbFloor (DoTs, reactions) in phases 1-2 queues the transition; the "흡수 중 (raw)" popup at most once per 10 t.
execute if score #mbFloorHit mb matches 1 run function rlk:boss/azhdaha/ev/pop
execute if score #azPh mb matches 1..2 if score #azTr mb matches 0 if score #mbFloor mb matches 1.. if score #mbFloorHit mb matches 1 run function rlk:boss/azhdaha/tr/queue
execute if score #azPh mb matches 1..2 if score #azTr mb matches 0 if score #mbFloor mb matches 1.. if score @s mhpC <= #mbFloor mb run function rlk:boss/azhdaha/tr/queue
scoreboard players set #mbFloorHit mb 0
execute if score #azTr mb matches 1.. if score #azPh mb matches 1..2 run scoreboard players set #azOrbHigh mb 1
