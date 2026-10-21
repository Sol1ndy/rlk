# GENERATED dispatcher: rlk:mboss/<id>/tick of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/tick
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/tick
execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/tick
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/tick
execute if score #mbId mb matches 98 run return run function rlk:mboss/cproto/tick
execute if score #mbId mb matches 11 run return run function rlk:mboss/apep/tick
