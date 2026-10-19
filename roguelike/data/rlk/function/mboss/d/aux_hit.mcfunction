# GENERATED dispatcher: rlk:mboss/<id>/aux_hit of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/aux_hit
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/aux_hit
execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/aux_hit
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/aux_hit
execute if score #mbId mb matches 98 run return run function rlk:mboss/cproto/aux_hit
