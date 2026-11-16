function rlk:mboss/lib_clear
execute if score #prPat mb matches 1.. run function rlk:mboss/proto/finish
function rlk:mboss/proto/pose/sink {d:8}
data modify storage rlk:mboss sub set value [{text:"그로기",color:"#FFD23F",bold:true}]
