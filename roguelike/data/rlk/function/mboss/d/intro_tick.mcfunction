# GENERATED dispatcher: rlk:mboss/<id>/intro_tick of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/intro_tick
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/intro_tick
execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/intro_tick
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/intro_tick
execute if score #mbId mb matches 98 run return run function rlk:mboss/cproto/intro_tick
