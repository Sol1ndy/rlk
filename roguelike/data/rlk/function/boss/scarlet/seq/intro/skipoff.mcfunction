# The intro skip prompt off for good (the window ended, the skip).
scoreboard players set #sq_skd hr 1
data modify storage rlk:mboss camtx.hint set value {text:"",background:0}
function rlk:mboss/cam/text
execute unless entity @a[tag=player,tag=rlk_mb_camh] run title @a[tag=player] actionbar ""
