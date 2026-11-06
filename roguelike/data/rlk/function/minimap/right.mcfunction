# /function rlk:minimap/right: nudge the minimap 10 GUI px to the right.
scoreboard players add #mmX mm 10
execute if score #mmX mm matches ..-1001 run scoreboard players set #mmX mm -1000
execute if score #mmX mm matches 1001.. run scoreboard players set #mmX mm 1000
scoreboard players set #mmSig mm -1
tellraw @s [{text:"[미니맵] ",color:"gold"},{text:"오른쪽으로 10칸 · 위치 x = ",color:"gray"},{score:{name:"#mmX",objective:"mm"},color:"white"}]
