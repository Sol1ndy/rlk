# GENERATED dispatcher: rlk:mboss/<id>/reload of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/reload
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/reload
execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/reload
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/reload
