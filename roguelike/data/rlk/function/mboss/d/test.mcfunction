# GENERATED dispatcher: rlk:<fn root>/test of the running boss (#mbId mb = registry n).
$execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/test {id:$(id)}
$execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/test {id:$(id)}
$execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/test {id:$(id)}
$execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/test {id:$(id)}
$execute if score #mbId mb matches 98 run return run function rlk:mboss/cproto/test {id:$(id)}
$execute if score #mbId mb matches 10 run return run function rlk:boss/azhdaha/test {id:$(id)}
$execute if score #mbId mb matches 11 run return run function rlk:boss/apep/test {id:$(id)}
$execute if score #mbId mb matches 20 run return run function rlk:boss/tachy/test {id:$(id)}
$execute if score #mbId mb matches 97 run return run function rlk:mboss/spproto/test {id:$(id)}
$scoreboard players set #mbReqT mb $(id)
