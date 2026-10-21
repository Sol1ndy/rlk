# STUB (AP-CORE, ap_contract 1.3): 근접 콤보 (combo, id 6); the pattern stage replaces this file.
# a 0-29, b 29-73, then c 73-93 + end 93-113 (3 hits) / end 73-93 (2) / d 93-170 (4)
execute if score #apPT mb matches 29 run function rlk:boss/apep/play/combo_b
execute if score #apq6 mb matches 2 if score #apPT mb matches 73 run function rlk:boss/apep/play/combo_end
execute if score #apq6 mb matches 3.. if score #apPT mb matches 73 run function rlk:boss/apep/play/combo_c
execute if score #apq6 mb matches 3 if score #apPT mb matches 93 run function rlk:boss/apep/play/combo_end
execute if score #apq6 mb matches 4 if score #apPT mb matches 93 run function rlk:boss/apep/play/combo_d
execute if score #apPT mb >= #apPLen mb run function rlk:boss/apep/p/end
