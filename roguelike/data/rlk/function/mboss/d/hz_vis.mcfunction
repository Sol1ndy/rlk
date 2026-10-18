# GENERATED dispatcher: rlk:mboss/<id>/hz_vis of the running mid-boss (#mbId mb = registry n).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/hz_vis
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/hz_vis
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/hz_vis
