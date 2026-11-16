# Removes the rig, the anchor marker, the face marker, the rig objectives and the rig storage (rlk:hr rig).
function rlk:boss/scarlet/rig/kill
kill @e[type=marker,tag=rlk_hr_face]
scoreboard objectives remove hrRigC
scoreboard objectives remove hrRigT
scoreboard objectives remove hrRigF
scoreboard objectives remove hrRigY
scoreboard objectives remove hrRigS
scoreboard objectives remove hrRigForm
scoreboard objectives remove hrRigPh
scoreboard objectives remove hrRigBl
scoreboard objectives remove hrRigFc
scoreboard objectives remove hrRigHR
scoreboard objectives remove hrRigHL
scoreboard objectives remove hrRigHat
scoreboard objectives remove hrRigSw
scoreboard objectives remove hrRigSc
scoreboard objectives remove hrRigPr
scoreboard objectives remove hrRigCu
scoreboard objectives remove hrRigBo
scoreboard objectives remove hrRigQ
scoreboard objectives remove hrRigQx
scoreboard objectives remove hrRigQy
scoreboard objectives remove hrRigQz
scoreboard objectives remove hrRigQw
data remove storage rlk:hr rig
