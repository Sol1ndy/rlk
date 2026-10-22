# Shared teardown: run flags off, room cleared (bars hidden by boss cleanup), lobby spawn.
scoreboard players set #rdTest rd 0
scoreboard players set #rdForce rd 0
scoreboard players set #rdLock rd 0
function rlk:run/end
function rlk:boss/raiden/cleanup
execute as @a[tag=player] run function rlk:lobby/go
