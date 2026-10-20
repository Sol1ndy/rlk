# GENERATED dispatcher: rlk:mboss/<id>/cleanup of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/cleanup
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/cleanup
execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/cleanup
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/cleanup
execute if score #mbId mb matches 98 run return run function rlk:mboss/cproto/cleanup
execute if score #mbId mb matches 10 run return run function rlk:mboss/azhdaha/cleanup
