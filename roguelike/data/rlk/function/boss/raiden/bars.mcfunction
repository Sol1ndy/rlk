bossbar set rlk:narukami players @a[tag=player]
bossbar set rlk:narukami visible true
bossbar set rlk:narukami_state players @a[tag=player]
bossbar set rlk:narukami_state visible true
scoreboard players set #rdBar rd 1
execute store result bossbar rlk:narukami max run scoreboard players get @s mhpM
execute store result bossbar rlk:narukami value run scoreboard players get @s mhpC
execute if score @s rdPhase matches 0 run bossbar set rlk:narukami_state max 600
execute if score @s rdPhase matches 0 store result bossbar rlk:narukami_state value run scoreboard players get @s rdRage
execute if score @s rdPhase matches 0..1 run bossbar set rlk:narukami_state name {text:"악연의 에너지",color:"light_purple"}
execute if score @s rdPhase matches 1 run bossbar set rlk:narukami_state max 56
execute if score @s rdPhase matches 1 store result bossbar rlk:narukami_state value run scoreboard players get @s rdTime
execute if score @s rdPhase matches 2 run bossbar set rlk:narukami_state max 750
execute if score @s rdPhase matches 2 store result bossbar rlk:narukami_state value run scoreboard players get @s rdShield
execute if score @s rdPhase matches 2 run bossbar set rlk:narukami_state name {text:"번개 갑주",color:"aqua"}
execute if score @s rdPhase matches 3 run bossbar set rlk:narukami_state name {text:"갑주 파괴",color:"green"}
execute if score @s rdPhase matches 3 run bossbar set rlk:narukami_state max 160
execute if score @s rdPhase matches 3 store result bossbar rlk:narukami_state value run scoreboard players get @s rdTime
