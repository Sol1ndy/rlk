# 바위가 닿음(부착 안 됨): 빙결(쇄빙) > 번개 > 불 > 물 > 얼음 순으로 결정
execute if score @s aVoid matches 1.. run return run function rlk:element/rx/void {e:"Void",n:5}
execute if score @s frzT matches 1.. run return run function rlk:element/rx/shatter
execute if score @s aThunder matches 1.. run return run function rlk:element/rx/crystal {e:"Thunder",n:3}
execute if score @s aFire matches 1.. run return run function rlk:element/rx/crystal {e:"Fire",n:1}
execute if score @s aWater matches 1.. run function rlk:element/lunar/sign
execute if score @s aWater matches 1.. if score #lnAll tmp matches 1 run scoreboard players set #lunRx tmp 26
execute if score @s aWater matches 1.. if score #lnAll tmp matches 1 run scoreboard players set @s lnCr 1
execute if score @s aWater matches 1.. run return run function rlk:element/rx/crystal {e:"Water",n:2}
execute if score @s aIce matches 1.. run return run function rlk:element/rx/crystal {e:"Ice",n:4}
