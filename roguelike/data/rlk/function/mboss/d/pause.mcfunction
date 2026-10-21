# GENERATED dispatcher: rlk:mboss/<id>/pause of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/pause
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/pause
execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/pause
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/pause
execute if score #mbId mb matches 98 run return run function rlk:mboss/cproto/pause
execute if score #mbId mb matches 10 run return run function rlk:mboss/azhdaha/pause
execute if score #mbId mb matches 11 run return run function rlk:mboss/apep/pause
