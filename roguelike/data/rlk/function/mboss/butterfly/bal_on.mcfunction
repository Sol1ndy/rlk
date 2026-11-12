# @s = body: cut what runs, human form, stand groggy.
function rlk:mboss/lib_clear
function rlk:mboss/butterfly/p/cancel
function rlk:mboss/butterfly/rig/prop/clear
scoreboard players set #bfMv mb 0
scoreboard players set #mbNoLeash mb 0
execute if score #bfForm mb matches 2 run scoreboard players set #bfHumN mb 0
execute if score #bfForm mb matches 2 run scoreboard players set #bfHumLim mb 4
execute if score #bfForm mb matches 2 run scoreboard players set #bfHumT mb 0
execute if score #bfForm mb matches 2 run scoreboard players set #bfHumTL mb 0
execute if score #bfForm mb matches 2 run function rlk:mboss/butterfly/form/now_h
function rlk:mboss/butterfly/rig/play/groggy_h
data modify storage rlk:mboss sub set value [{text:"그로기",color:"#FFD23F",bold:true}]
