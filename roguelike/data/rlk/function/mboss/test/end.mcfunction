scoreboard players set #mbTest mb 0
scoreboard players set #mbForce mb 0
scoreboard players set #mbLock mb 0
scoreboard players set #cbForce mb 0
scoreboard players set #cbAuto mb 0
function rlk:run/end
function rlk:mboss/cleanup
execute as @a[tag=player] run function rlk:lobby/go
