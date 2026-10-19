# GENERATED dispatcher: rlk:mboss/<id>/resume of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/resume
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/resume
execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/resume
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/resume
execute if score #mbId mb matches 98 run return run function rlk:mboss/cproto/resume
