# Internal, as the new card: spawn, end and fade-start time (#bfTcNow).
scoreboard players operation @s mbT = #bfTcT mb
scoreboard players operation #bfTcT mb += #bfTcL mb
scoreboard players operation @s mbS = #bfTcT mb
scoreboard players operation #bfTcT mb -= #bfTcF mb
scoreboard players operation @s mbId = #bfTcT mb
execute if score #bfTcF mb matches 1.. run tag @s add rlk_mb_bf_tcfd
