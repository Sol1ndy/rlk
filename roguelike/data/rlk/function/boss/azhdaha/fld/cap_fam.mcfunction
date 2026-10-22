# The family cap (fire 4, hail 2, strip 1): the oldest of the family goes when it is full.
scoreboard players set #azX mb 0
execute if score #azF0 mb = #azNfF mb run scoreboard players add #azX mb 1
execute if score #azF1 mb = #azNfF mb run scoreboard players add #azX mb 1
execute if score #azF2 mb = #azNfF mb run scoreboard players add #azX mb 1
execute if score #azF3 mb = #azNfF mb run scoreboard players add #azX mb 1
execute if score #azF4 mb = #azNfF mb run scoreboard players add #azX mb 1
execute if score #azF5 mb = #azNfF mb run scoreboard players add #azX mb 1
execute if score #azF6 mb = #azNfF mb run scoreboard players add #azX mb 1
execute if score #azF7 mb = #azNfF mb run scoreboard players add #azX mb 1
execute if score #azNfF mb matches 1 if score #azX mb matches 4.. run function rlk:boss/azhdaha/fld/cancel_oldest_fam
execute if score #azNfF mb matches 2 if score #azX mb matches 2.. run function rlk:boss/azhdaha/fld/cancel_oldest_fam
execute if score #azNfF mb matches 3 if score #azX mb matches 1.. run function rlk:boss/azhdaha/fld/cancel_oldest_fam
