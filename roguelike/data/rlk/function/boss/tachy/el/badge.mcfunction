# The element badge on the boss-bar name line (@s any).
execute if score #el tk matches 1 run data modify storage rlk:mboss extra set value [{text:"  ◈불",color:"#FF8A3D",bold:true}]
execute if score #el tk matches 3 run data modify storage rlk:mboss extra set value [{text:"  ◈번개",color:"#E8C84A",bold:true}]
