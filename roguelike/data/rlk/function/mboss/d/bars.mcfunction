# GENERATED dispatcher: rlk:mboss/<id>/bars of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/bars
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/bars
execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/bars
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/bars
execute if score #mbId mb matches 98 run return run function rlk:mboss/cproto/bars
execute if score #mbId mb matches 10 run return run function rlk:mboss/azhdaha/bars
execute if score #mbId mb matches 11 run return run function rlk:mboss/apep/bars
