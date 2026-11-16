# Called after normal damage/defense modifiers, before damage is deducted.
execute if score #dmg tmp matches ..0 run return 0
# Phase 0: rear-hit memory, the guard parry (번개 배리어) and the guard-break stun x1.5 (shogun.py).
execute if score @s rdPhase matches 0 run function rlk:boss/raiden/sg/incoming
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/shield_hit
execute if score @s rdPhase matches 3 run scoreboard players operation #dmg tmp += #dmg tmp
# The first transformation's HP gate: at or below 55 % HP she transforms at the next decision point (rage full). User
# 10-22 ("갑주 생성 전에 잡을 수도 있게"): the hit is NOT floored any more, so a burst can kill her before the Tenma
# armour exists (combat/apply runs death/start at 0 HP in phase 0 and in the transformation until its armour beat).
scoreboard players operation #rdFloor rd = @s mhpM
scoreboard players set #rdPct rd 55
scoreboard players operation #rdFloor rd *= #rdPct rd
scoreboard players operation #rdFloor rd /= #rd100 rd
scoreboard players operation #rdAfter rd = @s mhpC
scoreboard players operation #rdAfter rd -= #dmg tmp
execute if score @s rdPhase matches 0 if score @s rdCycle matches 0 if score #rdAfter rd <= #rdFloor rd run function rlk:boss/raiden/threshold
execute if score #dmg tmp matches 1.. run function rlk:boss/raiden/rig/flash
