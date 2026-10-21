# STUB (AP-CORE, ap_contract 1.3): 이동 돌진 (mstrike, id 31); the pattern stage replaces this file.
# keeps time only (the clip of each step at its clock; no hazards)
execute if score #apPT mb matches 32 run function rlk:boss/apep/p/mstrike/to_lock
execute if score #apPT mb matches 44 run execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score #apPT mb matches 72 run function rlk:boss/apep/p/release
execute if score #apPT mb matches 92.. run function rlk:boss/apep/p/end
