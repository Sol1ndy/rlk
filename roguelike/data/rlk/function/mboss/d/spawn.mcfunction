# GENERATED dispatcher: rlk:mboss/<id>/spawn of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/spawn
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/spawn
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/spawn
