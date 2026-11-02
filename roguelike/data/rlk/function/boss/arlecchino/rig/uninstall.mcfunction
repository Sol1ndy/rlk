# Removes the rig, the anchor marker, the face marker, the rig objectives and the rig storage (rlk:kn rig).
function rlk:boss/arlecchino/rig/kill
kill @e[type=marker,tag=rlk_kn_face]
scoreboard objectives remove knRigC
scoreboard objectives remove knRigT
scoreboard objectives remove knRigF
scoreboard objectives remove knRigY
scoreboard objectives remove knRigS
scoreboard objectives remove knRigForm
scoreboard objectives remove knRigWi
scoreboard objectives remove knRigWr
scoreboard objectives remove knRigWl
scoreboard objectives remove knRigGl
scoreboard objectives remove knRigPr
scoreboard objectives remove knRigFl
scoreboard objectives remove knRigQ
scoreboard objectives remove knRigQx
scoreboard objectives remove knRigQy
scoreboard objectives remove knRigQz
scoreboard objectives remove knRigQw
data remove storage rlk:kn rig
