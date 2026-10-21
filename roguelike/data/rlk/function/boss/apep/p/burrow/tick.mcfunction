# STUB (AP-CORE, ap_contract 1.3): 잠복 돌진 (burrow, id 1); the pattern stage replaces this file.
# keeps time only (the clip of each step at its clock; no hazards)
execute if score #apPT mb matches 32 run function rlk:boss/apep/p/burrow/to_lock
execute if score #apPT mb matches 44 run execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score #apPT mb matches 77 run function rlk:boss/apep/p/release
execute if score #apPT mb matches 82.. run function rlk:boss/apep/p/end
