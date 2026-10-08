# 공허가 닿음: 빙결·얼음 > 물 > 불 > 번개 > 풀·활성 순으로 공허 반응, 없으면 부착
execute if score @s frzT matches 1.. run return run function rlk:element/rx/void {e:"Ice",n:4}
execute if score @s aIce matches 1.. run return run function rlk:element/rx/void {e:"Ice",n:4}
execute if score @s aWater matches 1.. run return run function rlk:element/rx/void {e:"Water",n:2}
execute if score @s aFire matches 1.. run return run function rlk:element/rx/void {e:"Fire",n:1}
execute if score @s aThunder matches 1.. run return run function rlk:element/rx/void {e:"Thunder",n:3}
execute if score @s aGrass matches 1.. run return run function rlk:element/rx/void {e:"Grass",n:7}
execute if score @s quickT matches 1.. run return run function rlk:element/rx/void {e:"Grass",n:7}
function rlk:element/attach {e:"Void"}
