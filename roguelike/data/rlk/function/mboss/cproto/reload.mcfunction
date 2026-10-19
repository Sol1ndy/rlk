# Hook reload (@s = body): the rig, the module clocks; HP, the proxies (the framework) and the phase are kept.
scoreboard players set #cpPat mb 0
scoreboard players set #cpT mb 0
scoreboard players set #cpCool mb 40
scoreboard players set #cpFlash mb 0
execute unless score #cpPush mb matches 0..1 run scoreboard players set #cpPush mb 0
execute unless score #cpCine mb matches 0.. run scoreboard players set #cpCine mb 0
function rlk:mboss/cproto/rig/spawn
execute if score #mbSt mb matches 1 run function rlk:mboss/cproto/props/now
data modify storage rlk:mboss sub set value [{text:"대기",color:"#8A8A8A"}]
