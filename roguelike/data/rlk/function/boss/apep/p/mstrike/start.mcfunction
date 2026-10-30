# 이동 돌진 (mstrike, id 31; plan 8.3). move_strike_p3: sink 8, hidden 16-41, lock 32, burst 44, slam 61, sweep 69, end 92.
scoreboard players set #apq31O mb 0
execute if score @s apRigStance matches 0 run scoreboard players set #apq31O mb 14
execute if score #apq31O mb matches 14 run function rlk:boss/apep/play/stand_p3
execute if score #apq31O mb matches 14 run scoreboard players add #apPLen mb 14
scoreboard players operation #apq31T mb = #apPT mb
scoreboard players operation #apq31T mb -= #apq31O mb
kill @e[tag=rlk_mb_ap_p31]
scoreboard players set #apq31G mb 0
