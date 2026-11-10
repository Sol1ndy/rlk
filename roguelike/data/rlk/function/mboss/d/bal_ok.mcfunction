# GENERATED dispatcher: rlk:<fn root>/bal_ok of the running boss with the balance gauge (registry "bal").
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/bal_ok
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/bal_ok
execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/bal_ok
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/bal_ok
execute if score #mbId mb matches 98 run return run function rlk:mboss/cproto/bal_ok
execute if score #mbId mb matches 10 run return run function rlk:boss/azhdaha/bal_ok
execute if score #mbId mb matches 11 run return run function rlk:boss/apep/bal_ok
execute if score #mbId mb matches 20 run return run function rlk:boss/tachy/bal_ok
execute if score #mbId mb matches 97 run return run function rlk:mboss/spproto/bal_ok
execute if score #mbId mb matches 12 run return run function rlk:boss/arlecchino/bal_ok
execute if score #mbId mb matches 21 run return run function rlk:boss/scarlet/bal_ok
return fail
