# /function rlk:minimap/pos {x:N}: the map's left edge, GUI px from the screen centre
# (negative = left). Default -364.
$scoreboard players set #mmX mm $(x)
execute if score #mmX mm matches ..-1001 run scoreboard players set #mmX mm -1000
execute if score #mmX mm matches 1001.. run scoreboard players set #mmX mm 1000
scoreboard players set #mmSig mm -1
tellraw @s [{text:"[미니맵] ",color:"gold"},{text:"위치 x = ",color:"gray"},{score:{name:"#mmX",objective:"mm"},color:"white"}]
