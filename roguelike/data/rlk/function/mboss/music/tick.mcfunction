# From mboss/world (live, unpaused ticks) while #mbMusPh >= 1: the loop timer and the vanilla-music suppression.
scoreboard players add #mbMusT mb 1
execute if score #mbMusLen mb matches 1.. if score #mbMusT mb >= #mbMusLen mb run function rlk:mboss/music/loop
scoreboard players operation #t mb = #mbMusT mb
scoreboard players operation #t mb %= #c100 mb
execute if score #t mb matches 0 run stopsound @a[tag=player] music
