# GENERATED dispatcher: rlk:mboss/<id>/pause of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/pause
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/pause
