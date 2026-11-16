# Reload re-make of the emergence: the remaining tell (B3_BURST - 1 - #azPT, at least 1).
scoreboard players set #aq23T mb 387
scoreboard players operation #aq23T mb -= #azPT mb
execute if score #aq23T mb matches ..0 run scoreboard players set #aq23T mb 1
execute store result storage rlk:mboss az.p23.tell int 1 run scoreboard players get #aq23T mb
function rlk:boss/azhdaha/p/burrow3/emerge_m with storage rlk:mboss az.p23
