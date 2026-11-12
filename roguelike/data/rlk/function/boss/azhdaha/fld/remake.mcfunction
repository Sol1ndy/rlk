# /reload: every live field re-made from the table (the hazard with its remaining life, the card). The
# family volley groups start over once here (FIX STATE-15: the remade fields of a family share one group).
scoreboard players set #azFG1 mb 0
scoreboard players set #azFG2 mb 0
scoreboard players set #azFG3 mb 0
execute if score #azF0 mb matches 1.. run function rlk:boss/azhdaha/fld/remake_0
execute if score #azF1 mb matches 1.. run function rlk:boss/azhdaha/fld/remake_1
execute if score #azF2 mb matches 1.. run function rlk:boss/azhdaha/fld/remake_2
execute if score #azF3 mb matches 1.. run function rlk:boss/azhdaha/fld/remake_3
execute if score #azF4 mb matches 1.. run function rlk:boss/azhdaha/fld/remake_4
execute if score #azF5 mb matches 1.. run function rlk:boss/azhdaha/fld/remake_5
execute if score #azF6 mb matches 1.. run function rlk:boss/azhdaha/fld/remake_6
execute if score #azF7 mb matches 1.. run function rlk:boss/azhdaha/fld/remake_7
