scoreboard players add #gourdT itv 1
# #gourdInt 틱마다 회복 (강화 단계로 조정)
execute if score #gourdT itv >= #gourdInt tmp run function rlk:items/proc/gourd_heal
execute if score #gourdT itv >= #gourdInt tmp run scoreboard players set #gourdT itv 0
