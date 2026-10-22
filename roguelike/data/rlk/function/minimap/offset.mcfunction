# Append position spaces for an advance of 2 x |#mmX| (|#mmX| <= 1000): before the rows
# when #mmX > 0, after them when #mmX < 0 (see draw).
scoreboard players operation #len mm = #mmX mm
scoreboard players operation #len mm += #mmX mm
execute if score #len mm matches ..-1 run scoreboard players operation #len mm *= #neg mm
execute if score #len mm matches 1024.. run data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
execute if score #len mm matches 1024.. run scoreboard players remove #len mm 1024
execute if score #len mm matches 512.. run data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
execute if score #len mm matches 512.. run scoreboard players remove #len mm 512
execute if score #len mm matches 256.. run data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
execute if score #len mm matches 256.. run scoreboard players remove #len mm 256
execute if score #len mm matches 128.. run data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
execute if score #len mm matches 128.. run scoreboard players remove #len mm 128
execute if score #len mm matches 64.. run data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
execute if score #len mm matches 64.. run scoreboard players remove #len mm 64
execute if score #len mm matches 32.. run data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
execute if score #len mm matches 32.. run scoreboard players remove #len mm 32
execute if score #len mm matches 16.. run data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
execute if score #len mm matches 16.. run scoreboard players remove #len mm 16
execute if score #len mm matches 8.. run data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
execute if score #len mm matches 8.. run scoreboard players remove #len mm 8
execute if score #len mm matches 4.. run data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
execute if score #len mm matches 4.. run scoreboard players remove #len mm 4
execute if score #len mm matches 2.. run data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
execute if score #len mm matches 2.. run scoreboard players remove #len mm 2
execute if score #len mm matches 1.. run data modify storage rlk:mm line append value {text:"",font:"rlk:minimap"}
execute if score #len mm matches 1.. run scoreboard players remove #len mm 1
