# Hook reload (@s = body): the displays and the module clocks (HP is kept by the framework).
scoreboard players set #spPat mb 0
scoreboard players set #spT mb 0
scoreboard players set #spCool mb 40
scoreboard players set #spFlash mb 0
function rlk:mboss/spproto/rig/spawn
data modify storage rlk:mboss sub set value [{text:"균열 수호",color:"#8FD8FF"}]
