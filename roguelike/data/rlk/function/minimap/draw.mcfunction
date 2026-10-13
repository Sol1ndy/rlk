# Rebuild the minimap text (storage rlk:mm line) and put it on the boss bar.
scoreboard players operation #mmSig mm = #mmNew mm
scoreboard players set #mmAge mm 0
# Zone colour codes (#zc<k>) and door slots (#hd<i> right, #vd<i> below).
scoreboard players set #zc1 mm 0
scoreboard players set #zc2 mm 0
scoreboard players set #zc3 mm 0
scoreboard players set #zc4 mm 0
scoreboard players set #zc5 mm 0
scoreboard players set #zc6 mm 0
scoreboard players set #zc7 mm 0
scoreboard players set #zc8 mm 0
scoreboard players set #zc9 mm 0
scoreboard players set #zc10 mm 0
scoreboard players set #zc11 mm 0
scoreboard players set #zc12 mm 0
scoreboard players set #pz mm 0
execute if score #pc mm matches 0.. run function rlk:minimap/player_zone
execute as @e[tag=rlk_zone] run function rlk:minimap/zone_color
scoreboard players set #hd0 mm 0
scoreboard players set #vd0 mm 0
scoreboard players set #hd1 mm 0
scoreboard players set #vd1 mm 0
scoreboard players set #hd2 mm 0
scoreboard players set #vd2 mm 0
scoreboard players set #hd3 mm 0
scoreboard players set #vd3 mm 0
scoreboard players set #hd4 mm 0
scoreboard players set #vd4 mm 0
scoreboard players set #hd5 mm 0
scoreboard players set #vd5 mm 0
scoreboard players set #hd6 mm 0
scoreboard players set #vd6 mm 0
scoreboard players set #hd7 mm 0
scoreboard players set #vd7 mm 0
scoreboard players set #hd8 mm 0
scoreboard players set #vd8 mm 0
scoreboard players set #hd9 mm 0
scoreboard players set #vd9 mm 0
scoreboard players set #hd10 mm 0
scoreboard players set #vd10 mm 0
scoreboard players set #hd11 mm 0
scoreboard players set #vd11 mm 0
scoreboard players set #hd12 mm 0
scoreboard players set #vd12 mm 0
scoreboard players set #hd13 mm 0
scoreboard players set #vd13 mm 0
scoreboard players set #hd14 mm 0
scoreboard players set #vd14 mm 0
scoreboard players set #hd15 mm 0
scoreboard players set #vd15 mm 0
scoreboard players set #hd16 mm 0
scoreboard players set #vd16 mm 0
scoreboard players set #hd17 mm 0
scoreboard players set #vd17 mm 0
scoreboard players set #hd18 mm 0
scoreboard players set #vd18 mm 0
scoreboard players set #hd19 mm 0
scoreboard players set #vd19 mm 0
scoreboard players set #hd20 mm 0
scoreboard players set #vd20 mm 0
scoreboard players set #hd21 mm 0
scoreboard players set #vd21 mm 0
scoreboard players set #hd22 mm 0
scoreboard players set #vd22 mm 0
scoreboard players set #hd23 mm 0
scoreboard players set #vd23 mm 0
scoreboard players set #hd24 mm 0
scoreboard players set #vd24 mm 0
scoreboard players set #hd25 mm 0
scoreboard players set #vd25 mm 0
scoreboard players set #hd26 mm 0
scoreboard players set #vd26 mm 0
scoreboard players set #hd27 mm 0
scoreboard players set #vd27 mm 0
scoreboard players set #hd28 mm 0
scoreboard players set #vd28 mm 0
scoreboard players set #hd29 mm 0
scoreboard players set #vd29 mm 0
scoreboard players set #hd30 mm 0
scoreboard players set #vd30 mm 0
scoreboard players set #hd31 mm 0
scoreboard players set #vd31 mm 0
scoreboard players set #hd32 mm 0
scoreboard players set #vd32 mm 0
scoreboard players set #hd33 mm 0
scoreboard players set #vd33 mm 0
scoreboard players set #hd34 mm 0
scoreboard players set #vd34 mm 0
scoreboard players set #hd35 mm 0
scoreboard players set #vd35 mm 0
execute as @e[tag=rlk_door] run function rlk:minimap/door_slot
data modify storage rlk:mm line set value [{text:"",font:"rlk:minimap"}]
scoreboard players set #c mm 0
execute if score #g0 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g0 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g0 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g0 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g0 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g0 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g0 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g0 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g0 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g0 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g0 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g0 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/0
execute unless score #c mm matches 1.. if score #hd0 mm matches 1.. run function rlk:minimap/c/0
execute unless score #c mm matches 1.. if score #vd0 mm matches 1.. run function rlk:minimap/c/0
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g1 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g1 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g1 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g1 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g1 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g1 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g1 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g1 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g1 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g1 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g1 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g1 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/1
execute unless score #c mm matches 1.. if score #hd1 mm matches 1.. run function rlk:minimap/c/1
execute unless score #c mm matches 1.. if score #vd1 mm matches 1.. run function rlk:minimap/c/1
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g2 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g2 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g2 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g2 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g2 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g2 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g2 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g2 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g2 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g2 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g2 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g2 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/2
execute unless score #c mm matches 1.. if score #hd2 mm matches 1.. run function rlk:minimap/c/2
execute unless score #c mm matches 1.. if score #vd2 mm matches 1.. run function rlk:minimap/c/2
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g3 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g3 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g3 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g3 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g3 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g3 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g3 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g3 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g3 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g3 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g3 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g3 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/3
execute unless score #c mm matches 1.. if score #hd3 mm matches 1.. run function rlk:minimap/c/3
execute unless score #c mm matches 1.. if score #vd3 mm matches 1.. run function rlk:minimap/c/3
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g4 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g4 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g4 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g4 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g4 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g4 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g4 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g4 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g4 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g4 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g4 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g4 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/4
execute unless score #c mm matches 1.. if score #hd4 mm matches 1.. run function rlk:minimap/c/4
execute unless score #c mm matches 1.. if score #vd4 mm matches 1.. run function rlk:minimap/c/4
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g5 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g5 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g5 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g5 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g5 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g5 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g5 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g5 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g5 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g5 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g5 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g5 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/5
execute unless score #c mm matches 1.. if score #hd5 mm matches 1.. run function rlk:minimap/c/5
execute unless score #c mm matches 1.. if score #vd5 mm matches 1.. run function rlk:minimap/c/5
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g6 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g6 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g6 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g6 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g6 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g6 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g6 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g6 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g6 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g6 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g6 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g6 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/6
execute unless score #c mm matches 1.. if score #hd6 mm matches 1.. run function rlk:minimap/c/6
execute unless score #c mm matches 1.. if score #vd6 mm matches 1.. run function rlk:minimap/c/6
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g7 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g7 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g7 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g7 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g7 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g7 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g7 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g7 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g7 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g7 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g7 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g7 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/7
execute unless score #c mm matches 1.. if score #hd7 mm matches 1.. run function rlk:minimap/c/7
execute unless score #c mm matches 1.. if score #vd7 mm matches 1.. run function rlk:minimap/c/7
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g8 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g8 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g8 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g8 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g8 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g8 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g8 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g8 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g8 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g8 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g8 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g8 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/8
execute unless score #c mm matches 1.. if score #hd8 mm matches 1.. run function rlk:minimap/c/8
execute unless score #c mm matches 1.. if score #vd8 mm matches 1.. run function rlk:minimap/c/8
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g9 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g9 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g9 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g9 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g9 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g9 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g9 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g9 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g9 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g9 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g9 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g9 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/9
execute unless score #c mm matches 1.. if score #hd9 mm matches 1.. run function rlk:minimap/c/9
execute unless score #c mm matches 1.. if score #vd9 mm matches 1.. run function rlk:minimap/c/9
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g10 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g10 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g10 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g10 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g10 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g10 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g10 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g10 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g10 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g10 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g10 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g10 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/10
execute unless score #c mm matches 1.. if score #hd10 mm matches 1.. run function rlk:minimap/c/10
execute unless score #c mm matches 1.. if score #vd10 mm matches 1.. run function rlk:minimap/c/10
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g11 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g11 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g11 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g11 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g11 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g11 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g11 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g11 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g11 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g11 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g11 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g11 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/11
execute unless score #c mm matches 1.. if score #hd11 mm matches 1.. run function rlk:minimap/c/11
execute unless score #c mm matches 1.. if score #vd11 mm matches 1.. run function rlk:minimap/c/11
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g12 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g12 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g12 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g12 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g12 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g12 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g12 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g12 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g12 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g12 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g12 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g12 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/12
execute unless score #c mm matches 1.. if score #hd12 mm matches 1.. run function rlk:minimap/c/12
execute unless score #c mm matches 1.. if score #vd12 mm matches 1.. run function rlk:minimap/c/12
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g13 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g13 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g13 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g13 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g13 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g13 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g13 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g13 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g13 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g13 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g13 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g13 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/13
execute unless score #c mm matches 1.. if score #hd13 mm matches 1.. run function rlk:minimap/c/13
execute unless score #c mm matches 1.. if score #vd13 mm matches 1.. run function rlk:minimap/c/13
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g14 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g14 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g14 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g14 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g14 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g14 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g14 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g14 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g14 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g14 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g14 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g14 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/14
execute unless score #c mm matches 1.. if score #hd14 mm matches 1.. run function rlk:minimap/c/14
execute unless score #c mm matches 1.. if score #vd14 mm matches 1.. run function rlk:minimap/c/14
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g15 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g15 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g15 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g15 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g15 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g15 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g15 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g15 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g15 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g15 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g15 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g15 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/15
execute unless score #c mm matches 1.. if score #hd15 mm matches 1.. run function rlk:minimap/c/15
execute unless score #c mm matches 1.. if score #vd15 mm matches 1.. run function rlk:minimap/c/15
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g16 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g16 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g16 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g16 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g16 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g16 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g16 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g16 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g16 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g16 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g16 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g16 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/16
execute unless score #c mm matches 1.. if score #hd16 mm matches 1.. run function rlk:minimap/c/16
execute unless score #c mm matches 1.. if score #vd16 mm matches 1.. run function rlk:minimap/c/16
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g17 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g17 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g17 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g17 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g17 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g17 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g17 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g17 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g17 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g17 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g17 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g17 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/17
execute unless score #c mm matches 1.. if score #hd17 mm matches 1.. run function rlk:minimap/c/17
execute unless score #c mm matches 1.. if score #vd17 mm matches 1.. run function rlk:minimap/c/17
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g18 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g18 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g18 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g18 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g18 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g18 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g18 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g18 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g18 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g18 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g18 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g18 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/18
execute unless score #c mm matches 1.. if score #hd18 mm matches 1.. run function rlk:minimap/c/18
execute unless score #c mm matches 1.. if score #vd18 mm matches 1.. run function rlk:minimap/c/18
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g19 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g19 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g19 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g19 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g19 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g19 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g19 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g19 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g19 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g19 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g19 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g19 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/19
execute unless score #c mm matches 1.. if score #hd19 mm matches 1.. run function rlk:minimap/c/19
execute unless score #c mm matches 1.. if score #vd19 mm matches 1.. run function rlk:minimap/c/19
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g20 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g20 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g20 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g20 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g20 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g20 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g20 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g20 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g20 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g20 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g20 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g20 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/20
execute unless score #c mm matches 1.. if score #hd20 mm matches 1.. run function rlk:minimap/c/20
execute unless score #c mm matches 1.. if score #vd20 mm matches 1.. run function rlk:minimap/c/20
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g21 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g21 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g21 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g21 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g21 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g21 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g21 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g21 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g21 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g21 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g21 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g21 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/21
execute unless score #c mm matches 1.. if score #hd21 mm matches 1.. run function rlk:minimap/c/21
execute unless score #c mm matches 1.. if score #vd21 mm matches 1.. run function rlk:minimap/c/21
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g22 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g22 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g22 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g22 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g22 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g22 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g22 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g22 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g22 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g22 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g22 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g22 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/22
execute unless score #c mm matches 1.. if score #hd22 mm matches 1.. run function rlk:minimap/c/22
execute unless score #c mm matches 1.. if score #vd22 mm matches 1.. run function rlk:minimap/c/22
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g23 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g23 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g23 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g23 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g23 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g23 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g23 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g23 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g23 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g23 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g23 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g23 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/23
execute unless score #c mm matches 1.. if score #hd23 mm matches 1.. run function rlk:minimap/c/23
execute unless score #c mm matches 1.. if score #vd23 mm matches 1.. run function rlk:minimap/c/23
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g24 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g24 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g24 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g24 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g24 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g24 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g24 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g24 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g24 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g24 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g24 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g24 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/24
execute unless score #c mm matches 1.. if score #hd24 mm matches 1.. run function rlk:minimap/c/24
execute unless score #c mm matches 1.. if score #vd24 mm matches 1.. run function rlk:minimap/c/24
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g25 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g25 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g25 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g25 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g25 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g25 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g25 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g25 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g25 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g25 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g25 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g25 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/25
execute unless score #c mm matches 1.. if score #hd25 mm matches 1.. run function rlk:minimap/c/25
execute unless score #c mm matches 1.. if score #vd25 mm matches 1.. run function rlk:minimap/c/25
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g26 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g26 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g26 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g26 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g26 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g26 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g26 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g26 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g26 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g26 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g26 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g26 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/26
execute unless score #c mm matches 1.. if score #hd26 mm matches 1.. run function rlk:minimap/c/26
execute unless score #c mm matches 1.. if score #vd26 mm matches 1.. run function rlk:minimap/c/26
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g27 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g27 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g27 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g27 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g27 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g27 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g27 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g27 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g27 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g27 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g27 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g27 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/27
execute unless score #c mm matches 1.. if score #hd27 mm matches 1.. run function rlk:minimap/c/27
execute unless score #c mm matches 1.. if score #vd27 mm matches 1.. run function rlk:minimap/c/27
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g28 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g28 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g28 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g28 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g28 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g28 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g28 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g28 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g28 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g28 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g28 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g28 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/28
execute unless score #c mm matches 1.. if score #hd28 mm matches 1.. run function rlk:minimap/c/28
execute unless score #c mm matches 1.. if score #vd28 mm matches 1.. run function rlk:minimap/c/28
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g29 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g29 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g29 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g29 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g29 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g29 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g29 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g29 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g29 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g29 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g29 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g29 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/29
execute unless score #c mm matches 1.. if score #hd29 mm matches 1.. run function rlk:minimap/c/29
execute unless score #c mm matches 1.. if score #vd29 mm matches 1.. run function rlk:minimap/c/29
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g30 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g30 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g30 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g30 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g30 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g30 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g30 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g30 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g30 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g30 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g30 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g30 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/30
execute unless score #c mm matches 1.. if score #hd30 mm matches 1.. run function rlk:minimap/c/30
execute unless score #c mm matches 1.. if score #vd30 mm matches 1.. run function rlk:minimap/c/30
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g31 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g31 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g31 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g31 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g31 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g31 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g31 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g31 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g31 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g31 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g31 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g31 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/31
execute unless score #c mm matches 1.. if score #hd31 mm matches 1.. run function rlk:minimap/c/31
execute unless score #c mm matches 1.. if score #vd31 mm matches 1.. run function rlk:minimap/c/31
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g32 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g32 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g32 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g32 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g32 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g32 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g32 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g32 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g32 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g32 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g32 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g32 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/32
execute unless score #c mm matches 1.. if score #hd32 mm matches 1.. run function rlk:minimap/c/32
execute unless score #c mm matches 1.. if score #vd32 mm matches 1.. run function rlk:minimap/c/32
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g33 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g33 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g33 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g33 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g33 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g33 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g33 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g33 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g33 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g33 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g33 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g33 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/33
execute unless score #c mm matches 1.. if score #hd33 mm matches 1.. run function rlk:minimap/c/33
execute unless score #c mm matches 1.. if score #vd33 mm matches 1.. run function rlk:minimap/c/33
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g34 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g34 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g34 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g34 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g34 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g34 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g34 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g34 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g34 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g34 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g34 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g34 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/34
execute unless score #c mm matches 1.. if score #hd34 mm matches 1.. run function rlk:minimap/c/34
execute unless score #c mm matches 1.. if score #vd34 mm matches 1.. run function rlk:minimap/c/34
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
scoreboard players set #c mm 0
execute if score #g35 mm matches 1 run scoreboard players operation #c mm = #zc1 mm
execute if score #g35 mm matches 2 run scoreboard players operation #c mm = #zc2 mm
execute if score #g35 mm matches 3 run scoreboard players operation #c mm = #zc3 mm
execute if score #g35 mm matches 4 run scoreboard players operation #c mm = #zc4 mm
execute if score #g35 mm matches 5 run scoreboard players operation #c mm = #zc5 mm
execute if score #g35 mm matches 6 run scoreboard players operation #c mm = #zc6 mm
execute if score #g35 mm matches 7 run scoreboard players operation #c mm = #zc7 mm
execute if score #g35 mm matches 8 run scoreboard players operation #c mm = #zc8 mm
execute if score #g35 mm matches 9 run scoreboard players operation #c mm = #zc9 mm
execute if score #g35 mm matches 10 run scoreboard players operation #c mm = #zc10 mm
execute if score #g35 mm matches 11 run scoreboard players operation #c mm = #zc11 mm
execute if score #g35 mm matches 12 run scoreboard players operation #c mm = #zc12 mm
execute if score #c mm matches 1.. run function rlk:minimap/c/35
execute unless score #c mm matches 1.. if score #hd35 mm matches 1.. run function rlk:minimap/c/35
execute unless score #c mm matches 1.. if score #vd35 mm matches 1.. run function rlk:minimap/c/35
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
bossbar set rlk:minimap name {nbt:"line[]",storage:"rlk:mm",interpret:true,separator:""}
