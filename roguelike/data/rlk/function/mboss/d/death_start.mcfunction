# GENERATED dispatcher: rlk:mboss/<id>/death_start of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/death_start
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/death_start
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/death_start
