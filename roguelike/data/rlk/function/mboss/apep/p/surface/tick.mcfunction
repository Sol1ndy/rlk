# STUB (AP-CORE, ap_contract 1.3): 수면 포격 (surface, id 36); the pattern stage replaces this file.
# keeps time only (the clip of each step at its clock; no hazards)
execute if score #apPT mb matches 30 run function rlk:mboss/apep/p/surface/to_lock
execute if score #apPT mb matches 36 run function rlk:mboss/apep/play/surface_p3
execute if score #apPT mb matches 49 run function rlk:mboss/apep/p/release
execute if score #apPT mb matches 90.. run function rlk:mboss/apep/p/end
