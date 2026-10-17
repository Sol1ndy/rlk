# GENERATED dispatcher: rlk:mboss/<id>/test of the running mid-boss (#mbId mb = registry n).
$execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/test {id:$(id)}
$execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/test {id:$(id)}
$scoreboard players set #mbReqT mb $(id)
