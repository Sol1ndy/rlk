# @s = body: cut what runs, slump.
function rlk:mboss/lib_clear
function rlk:mboss/fieldgen/p/cancel
function rlk:mboss/fieldgen/rig/prop/clear
function rlk:mboss/fieldgen/fx/tele/clear
function rlk:mboss/fieldgen/hud/banner_cut
scoreboard players set #fgMv mb 0
scoreboard players set #mbNoLeash mb 0
scoreboard players set #fgT mb 0
function rlk:mboss/fieldgen/groggy/rig
data modify storage rlk:mboss sub set value [{text:"그로기",color:"#FFD23F",bold:true}]
