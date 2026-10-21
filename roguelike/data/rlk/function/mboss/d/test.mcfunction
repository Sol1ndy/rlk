# GENERATED dispatcher: rlk:mboss/<id>/test of the running mid-boss (#mbId mb = registry n).
$execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/test {id:$(id)}
$execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/test {id:$(id)}
$execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/test {id:$(id)}
$execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/test {id:$(id)}
$execute if score #mbId mb matches 98 run return run function rlk:mboss/cproto/test {id:$(id)}
$execute if score #mbId mb matches 11 run return run function rlk:mboss/apep/test {id:$(id)}
$scoreboard players set #mbReqT mb $(id)
