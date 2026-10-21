# @s = body (phase 1): the floor (plan 7.2): a hit with mhpC - raw <= #mbFloor (#mbFloorHit, framework) or mhpC <=
# #mbFloor (DoTs, reactions) queues the transition (#apTr 1); a released pattern ends now; the popup "…" at most
# once per 10 t while clamped.
execute if score #mbFloorHit mb matches 1 run function rlk:mboss/apep/ev/pop
execute if score #apTr mb matches 0 if score #mbFloor mb matches 1.. if score #mbFloorHit mb matches 1 run function rlk:mboss/apep/tr/queue
execute if score #apTr mb matches 0 if score #mbFloor mb matches 1.. if score @s mhpC <= #mbFloor mb run function rlk:mboss/apep/tr/queue
scoreboard players set #mbFloorHit mb 0
