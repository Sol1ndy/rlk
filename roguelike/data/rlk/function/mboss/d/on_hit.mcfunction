# GENERATED dispatcher: rlk:<fn root>/on_hit of the running boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/on_hit
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/on_hit
execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/on_hit
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/on_hit
execute if score #mbId mb matches 98 run return run function rlk:mboss/cproto/on_hit
execute if score #mbId mb matches 10 run return run function rlk:boss/azhdaha/on_hit
execute if score #mbId mb matches 11 run return run function rlk:boss/apep/on_hit
execute if score #mbId mb matches 97 run return run function rlk:mboss/spproto/on_hit
