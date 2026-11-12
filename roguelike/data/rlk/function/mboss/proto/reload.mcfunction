# Hook reload (@s = body): AI to idle, rig rebuilt; HP kept.
scoreboard players set #prPat mb 0
scoreboard players set #prT mb 0
scoreboard players set #prGo mb 0
scoreboard players set #prReq mb 0
scoreboard players set #prCool mb 30
scoreboard players set #prFlash mb 0
scoreboard players set #c3 mb 3
function rlk:mboss/proto/rig/spawn
data modify storage rlk:mboss sub set value [{text:"대기",color:"#8A8A8A"}]
