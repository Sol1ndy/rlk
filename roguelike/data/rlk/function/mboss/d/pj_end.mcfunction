# GENERATED dispatcher: rlk:mboss/<id>/pj_end of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/pj_end
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/pj_end
execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/pj_end
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/pj_end
execute if score #mbId mb matches 98 run return run function rlk:mboss/cproto/pj_end
