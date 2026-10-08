# 부착 원소 아이콘 표시 (@s = 몹 → 머리 위, 플레이어 → 액션바). 구성이 바뀔 때만 갱신
scoreboard players set #ik tmp 0
execute if score @s aFire matches 1.. run scoreboard players add #ik tmp 1
execute if score @s aWater matches 1.. run scoreboard players add #ik tmp 2
execute if score @s aThunder matches 1.. run scoreboard players add #ik tmp 4
execute if score @s aIce matches 1.. run scoreboard players add #ik tmp 8
execute if score @s aGrass matches 1.. run scoreboard players add #ik tmp 16
execute if score @s frzT matches 1.. run scoreboard players add #ik tmp 32
execute if score @s quickT matches 1.. run scoreboard players add #ik tmp 64
execute if score @s aVoid matches 1.. run scoreboard players add #ik tmp 128
scoreboard players operation #ikE tmp = @s rnEr
scoreboard players operation #ikE tmp *= #c256 tmp
scoreboard players operation #ik tmp += #ikE tmp
execute if score #ik tmp = @s icKey run return 0
scoreboard players operation @s icKey = #ik tmp
data modify storage rlk:st ic set value []
execute if score @s aFire matches 1.. run data modify storage rlk:st ic append value {text:"🔥 ",color:"#FF8A3D"}
execute if score @s aWater matches 1.. run data modify storage rlk:st ic append value {text:"🌊 ",color:"#4FB8FF"}
execute if score @s aThunder matches 1.. run data modify storage rlk:st ic append value {text:"⚡ ",color:"#C58BFF"}
execute if score @s aIce matches 1.. run data modify storage rlk:st ic append value {text:"❄ ",color:"#9FE8F5"}
execute if score @s aGrass matches 1.. run data modify storage rlk:st ic append value {text:"♣ ",color:"#A5D94A"}
execute if score @s frzT matches 1.. run data modify storage rlk:st ic append value {text:"[빙결] ",color:"#E6F7FF",bold:true}
execute if score @s quickT matches 1.. run data modify storage rlk:st ic append value {text:"[활성] ",color:"#C8E64A"}
execute if score @s aVoid matches 1.. run data modify storage rlk:st ic append value {text:"◉ ",color:"#E0365F"}
execute if entity @s[type=minecraft:player] run return run data modify storage rlk:hud aura set from storage rlk:st ic
# 로노바의 잠식 게이지(체력 바에 붙음)
function rlk:element/void/er_gauge
execute on passengers if entity @s[tag=rlk_hb_icon] if data storage rlk:st ic[0] run function rlk:element/set_icon with storage rlk:st
execute on passengers if entity @s[tag=rlk_hb_icon] unless data storage rlk:st ic[0] run data modify entity @s text set value {text:""}
