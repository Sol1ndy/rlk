# #pc = row * 6 + col, #mmDir: the strings around the arrow and its glyph, then append.
scoreboard players set #c6 mm 6
scoreboard players set #c16 mm 16
scoreboard players operation #acol mm = #pc mm
scoreboard players operation #acol mm %= #c6 mm
scoreboard players operation #ak mm = #pc mm
scoreboard players operation #ak mm /= #c6 mm
scoreboard players operation #ak mm *= #c16 mm
scoreboard players operation #ak mm += #mmDir mm
execute if score #acol mm matches 0 run data modify storage rlk:mm a set value {pre:"",post:""}
execute if score #acol mm matches 1 run data modify storage rlk:mm a set value {pre:"",post:""}
execute if score #acol mm matches 2 run data modify storage rlk:mm a set value {pre:"",post:""}
execute if score #acol mm matches 3 run data modify storage rlk:mm a set value {pre:"",post:""}
execute if score #acol mm matches 4 run data modify storage rlk:mm a set value {pre:"",post:""}
execute if score #acol mm matches 5 run data modify storage rlk:mm a set value {pre:"",post:""}
execute if score #ak mm matches 0 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 1 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 2 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 3 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 4 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 5 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 6 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 7 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 16 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 17 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 18 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 19 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 20 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 21 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 22 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 23 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 32 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 33 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 34 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 35 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 36 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 37 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 38 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 39 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 48 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 49 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 50 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 51 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 52 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 53 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 54 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 55 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 64 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 65 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 66 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 67 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 68 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 69 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 70 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 71 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 80 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 81 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 82 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 83 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 84 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 85 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 86 run data modify storage rlk:mm a.g set value ""
execute if score #ak mm matches 87 run data modify storage rlk:mm a.g set value ""
function rlk:minimap/arrow_add with storage rlk:mm a
