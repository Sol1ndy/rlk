execute unless score #mbLn mb matches 1 run return 0
execute if entity @a[tag=player,scores={dead=1}] run return 0
scoreboard players add #mbLnT mb 1
execute if score #mbLnT mb >= #mbLnGap mb run function rlk:mboss/line/next
