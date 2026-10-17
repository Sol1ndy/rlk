# GENERATED dispatcher: rlk:mboss/<id>/on_hit of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/on_hit
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/on_hit
