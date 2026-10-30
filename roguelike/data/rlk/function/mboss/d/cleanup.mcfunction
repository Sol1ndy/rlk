# GENERATED dispatcher: rlk:<fn root>/cleanup of the running boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/cleanup
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/cleanup
execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/cleanup
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/cleanup
execute if score #mbId mb matches 98 run return run function rlk:mboss/cproto/cleanup
execute if score #mbId mb matches 10 run return run function rlk:boss/azhdaha/cleanup
execute if score #mbId mb matches 11 run return run function rlk:boss/apep/cleanup
execute if score #mbId mb matches 20 run return run function rlk:boss/tachy/cleanup
execute if score #mbId mb matches 97 run return run function rlk:mboss/spproto/cleanup
