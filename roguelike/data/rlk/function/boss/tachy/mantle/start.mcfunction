# G2 과부하 외피 (@s = body; the phase step reserved by a floor: #flnext 1 = M1 at 70 %, 2 = M2 at 35 %). She wraps
# herself in the wings; gauge 100, she takes 20 % damage, time 360 / 300 t;
# the HP floor moves to the next one (M1: 35 %; M2: 1 HP until P3) so the mantle damage counts.
execute if score #flnext tk matches 1 run scoreboard players set #ph tk 2
execute if score #flnext tk matches 1 run scoreboard players set #sht tk 360
execute if score #flnext tk matches 1 run scoreboard players operation #mbFloor mb = #fl35 tk
execute if score #flnext tk matches 2.. run scoreboard players set #ph tk 5
execute if score #flnext tk matches 2.. run scoreboard players set #sht tk 300
execute if score #flnext tk matches 2.. run scoreboard players set #mbFloor mb 1
scoreboard players set #flnext tk 0
scoreboard players set #pat tk 51
scoreboard players set #pt tk 0
scoreboard players set #sh tk 100
scoreboard players set #shicd tk 0
scoreboard players set #taken tk 20
scoreboard players set #core tk 1
scoreboard players set #hud_g tk -1
scoreboard players set #hud_c tk -1
tag @s remove rlk_tk_core
tag @s add rlk_tk_mantle
function rlk:boss/tachy/rig_stub/play/mantle_in
execute at @s run playsound minecraft:item.elytra.flying hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
execute at @s run playsound minecraft:block.beacon.ambient hostile @a[tag=player] ~ ~ ~ 0.6 1.6 0.2
data modify storage rlk:mboss extra set value [{text:"  ◈외피",color:"#F2C230",bold:true}]
function rlk:boss/tachy/mantle/gauge
function rlk:boss/tachy/hud/sub
