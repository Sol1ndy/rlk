# STUB (AP-CORE, ap_contract 1.3): 잠복 이동 (reloc, id 7); the pattern stage replaces this file.
# keeps time only (the clip of each step at its clock; no hazards)
execute if score #apPT mb matches 17 run function rlk:boss/apep/p/reloc/to_lock
execute if score #apPT mb matches 18 run function rlk:boss/apep/play/emerge_on_p1
execute if score #apPT mb matches 42.. run function rlk:boss/apep/p/end
