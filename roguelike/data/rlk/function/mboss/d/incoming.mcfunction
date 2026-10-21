# GENERATED dispatcher: rlk:mboss/<id>/incoming of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/incoming
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/incoming
execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/incoming
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/incoming
execute if score #mbId mb matches 98 run return run function rlk:mboss/cb/inc/cproto
execute if score #mbId mb matches 10 run return run function rlk:mboss/cb/inc/azhdaha
execute if score #mbId mb matches 11 run return run function rlk:mboss/cb/inc/apep
