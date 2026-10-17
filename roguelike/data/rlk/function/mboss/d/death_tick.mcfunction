# GENERATED dispatcher: rlk:mboss/<id>/death_tick of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/death_tick
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/death_tick
