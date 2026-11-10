# GENERATED dispatcher: rlk:<fn root>/tick of the running boss (#mbId mb = registry n).
# balance gauge (registry "bal", mboss_lib.BAL_HOOKS): a groggy body (@s grgT >= 1) runs its bal_tick instead (last line: no extra command otherwise)
execute if score #mbId mb matches 1 unless score @s grgT matches 1.. run return run function rlk:mboss/guardian/tick
execute if score #mbId mb matches 2 unless score @s grgT matches 1.. run return run function rlk:mboss/butterfly/tick
execute if score #mbId mb matches 3 unless score @s grgT matches 1.. run return run function rlk:mboss/fieldgen/tick
execute if score #mbId mb matches 99 unless score @s grgT matches 1.. run return run function rlk:mboss/proto/tick
execute if score #mbId mb matches 98 unless score @s grgT matches 1.. run return run function rlk:mboss/cproto/tick
execute if score #mbId mb matches 10 unless score @s grgT matches 1.. run return run function rlk:boss/azhdaha/tick
execute if score #mbId mb matches 11 unless score @s grgT matches 1.. run return run function rlk:boss/apep/tick
execute if score #mbId mb matches 20 unless score @s grgT matches 1.. run return run function rlk:boss/tachy/tick
execute if score #mbId mb matches 97 unless score @s grgT matches 1.. run return run function rlk:mboss/spproto/tick
execute if score #mbId mb matches 12 unless score @s grgT matches 1.. run return run function rlk:boss/arlecchino/tick
execute if score #mbId mb matches 21 unless score @s grgT matches 1.. run return run function rlk:boss/scarlet/tick
execute if score @s grgT matches 1.. run return run function rlk:mboss/d/bal_tick
