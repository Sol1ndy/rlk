# Hook bars (@s = body): the phase on the sub-line, the pool split on the under-bar (gold), HP colour code 3 in phase 2.
execute if score #cpPh mb matches 2 run scoreboard players set #buHpCol bu 3
execute if score #cpPh mb matches 1 run data modify storage rlk:mboss sub set value [{text:"1단계",color:"#9FC6E8"}]
execute if score #cpPh mb matches 2 run data modify storage rlk:mboss sub set value [{text:"2단계",color:"#E8A0A0"}]
