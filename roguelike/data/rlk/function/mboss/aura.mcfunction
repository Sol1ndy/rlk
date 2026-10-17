# @s = body. Element auras as glyphs on the name line (the body has no overhead bar). Rebuilt on change.
scoreboard players set #k mb 0
execute if score @s aFire matches 1.. run scoreboard players add #k mb 1
execute if score @s aWater matches 1.. run scoreboard players add #k mb 2
execute if score @s aThunder matches 1.. run scoreboard players add #k mb 4
execute if score @s aIce matches 1.. run scoreboard players add #k mb 8
execute if score @s aGrass matches 1.. run scoreboard players add #k mb 16
execute if score @s aVoid matches 1.. run scoreboard players add #k mb 32
execute if score @s frzT matches 1.. run scoreboard players add #k mb 64
execute if score #k mb = #mbAuraK mb run return 0
scoreboard players operation #mbAuraK mb = #k mb
data modify storage rlk:mboss aura set value []
execute if score @s aFire matches 1.. run data modify storage rlk:mboss aura append value {text:"  🔥",color:"#FF8A3D"}
execute if score @s aWater matches 1.. run data modify storage rlk:mboss aura append value {text:"  🌊",color:"#4FB8FF"}
execute if score @s aThunder matches 1.. run data modify storage rlk:mboss aura append value {text:"  ⚡",color:"#C58BFF"}
execute if score @s aIce matches 1.. run data modify storage rlk:mboss aura append value {text:"  ❄",color:"#9FE8F5"}
execute if score @s aGrass matches 1.. run data modify storage rlk:mboss aura append value {text:"  ♣",color:"#A5D94A"}
execute if score @s aVoid matches 1.. run data modify storage rlk:mboss aura append value {text:"  ◉",color:"#E0365F"}
execute if score @s frzT matches 1.. run data modify storage rlk:mboss aura append value {text:"  [빙결]",color:"#E6F7FF",bold:true}
