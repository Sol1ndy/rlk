function rlk:boss/raiden/line/tick
execute if score #rdCap rd matches 1 unless entity @a[tag=player,scores={ttlT=1..}] run function rlk:boss/raiden/caption/expire
bossbar set rlk:narukami players @a[tag=player]
bossbar set rlk:narukami visible true
bossbar set rlk:narukami_state players @a[tag=player]
bossbar set rlk:narukami_state visible true
scoreboard players set #rdBar rd 1
# Line 1: level and name (and the armour state). Line 2: the drawn HP bar, numbers on it,
# the white recent-damage trail, and under it the malice gauge / armour / recovery.
execute unless score @s rdPhase matches 2..3 run bossbar set rlk:narukami name [{text:"Lv.",color:"#FFD86B",bold:true},{score:{name:"@s",objective:"mlv"},color:"#FFD86B",bold:true},{text:"  마가츠 미타케 나루카미노 미코토",color:"#E6C8FF"}]
execute if score @s rdPhase matches 2 run bossbar set rlk:narukami name [{text:"Lv.",color:"#FFD86B",bold:true},{score:{name:"@s",objective:"mlv"},color:"#FFD86B",bold:true},{text:"  마가츠 미타케 나루카미노 미코토",color:"#E6C8FF"},{text:"  · 번개 갑주",color:"#C58BFF"}]
execute if score @s rdPhase matches 3 run bossbar set rlk:narukami name [{text:"Lv.",color:"#FFD86B",bold:true},{score:{name:"@s",objective:"mlv"},color:"#FFD86B",bold:true},{text:"  마가츠 미타케 나루카미노 미코토",color:"#E6C8FF"},{text:"  · 갑주 파괴",color:"#7BD88F"}]
scoreboard players operation #buHp bu = @s mhpC
scoreboard players operation #buMax bu = @s mhpM
scoreboard players set #buSubCol bu 0
execute if score @s rdPhase matches 0 run scoreboard players operation #buSub bu = @s rdRage
execute if score @s rdPhase matches 0 run scoreboard players set #buSubMax bu 900
execute if score @s rdPhase matches 0 run scoreboard players set #buSubCol bu 8
execute if score @s rdPhase matches 1 run scoreboard players operation #buSub bu = @s rdTime
execute if score @s rdPhase matches 1 run scoreboard players set #buSubMax bu 52
execute if score @s rdPhase matches 1 run scoreboard players set #buSubCol bu 1
execute if score @s rdPhase matches 2 run scoreboard players operation #buSub bu = @s rdShield
execute if score @s rdPhase matches 2 run scoreboard players set #buSubMax bu 750
execute if score @s rdPhase matches 2 run scoreboard players set #buSubCol bu 1
execute if score @s rdPhase matches 3 run scoreboard players operation #buSub bu = @s rdTime
execute if score @s rdPhase matches 3 run scoreboard players set #buSubMax bu 300
execute if score @s rdPhase matches 3 run scoreboard players set #buSubCol bu 9
function rlk:bossui/draw
bossbar set rlk:narukami_state name {nbt:"line[]",storage:"rlk:bu",interpret:true,separator:""}
