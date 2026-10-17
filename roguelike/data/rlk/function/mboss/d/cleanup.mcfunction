# GENERATED dispatcher: rlk:mboss/<id>/cleanup of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/cleanup
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/cleanup
