# @s = the 중간보스 zone marker, at @s (from room/combat_clear: the body is gone, #combat is 0).
# #mbKilled 1 = killed through combat/apply (reward); anything else (/kill, failed spawn, a reload that
# lost the body) cancels: no reward, the gate comes back so the fight can be retried.
scoreboard players operation #mbWas mb = #mbOn mb
execute in minecraft:overworld run function rlk:mboss/ar/box_absorb
function rlk:mboss/cleanup_fight
execute unless data storage rlk:mboss ret.x run function rlk:mboss/ret_here
execute if score #mbWas mb matches 1 as @a[tag=player,limit=1] run function rlk:mboss/tp_out
scoreboard players set #mbRegate mb 0
execute if score #mbKilled mb matches 1 run function rlk:mboss/reward
execute unless score #mbKilled mb matches 1 run function rlk:mboss/cancelled
execute if score #mbTest mb matches 1 if data storage rlk:mboss cur run function rlk:mboss/test/won with storage rlk:mboss cur
function rlk:mboss/forget
execute if score #mbRegate mb matches 1 run function rlk:room/obj/k_mboss
