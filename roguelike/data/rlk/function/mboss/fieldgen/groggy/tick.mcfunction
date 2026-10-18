scoreboard players add #fgT mb 1
scoreboard players operation #fgM mb = #fgT mb
scoreboard players operation #fgM mb %= #fgK20 mb
execute if score #fgM mb matches 0 run function rlk:mboss/fieldgen/cfx/groggy_spark
execute if score #fgT mb matches 200.. run function rlk:mboss/fieldgen/recover/begin
