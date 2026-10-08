# 바람이 닿음(부착 안 됨): 번개 > 불 > 물 > 얼음·빙결 순으로 확산
execute if score @s aVoid matches 1.. run return run function rlk:element/rx/void {e:"Void",n:6}
execute if score @s aThunder matches 1.. run return run function rlk:element/rx/swirl {e:"Thunder",n:3}
execute if score @s aFire matches 1.. run return run function rlk:element/rx/swirl {e:"Fire",n:1}
execute if score @s aWater matches 1.. run return run function rlk:element/rx/swirl {e:"Water",n:2}
execute if score @s aIce matches 1.. run return run function rlk:element/rx/swirl {e:"Ice",n:4}
execute if score @s frzT matches 1.. run return run function rlk:element/rx/swirl {e:"Ice",n:4}
