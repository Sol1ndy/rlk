# 검신합일 · 체력이 낮을 때 (@s = 플레이어, hw_stat 에서 2틱마다): 치명타 피해 +#hwLowCd, 20틱마다 몸에 보랏빛 입자(hw_pulse)
scoreboard players operation @s critDamage += #hwLowCd tmp
scoreboard players add #hwPulse itv 1
execute if score #hwPulse itv matches 10.. at @e[tag=rlk_body,limit=1] run function rlk:items/proc/hw_pulse
