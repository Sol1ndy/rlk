# 홍련일섬 치명타 확률 시간 (@s = 플레이어, hw_due: 10틱마다와 끝나는 시각): 끝났으면 끄고, 아니면 몸에 번개 불꽃 2개
execute if score #hwNow itv >= #hwCritEnd itv run return run scoreboard players set #hwCritT itv 0
execute at @e[tag=rlk_body,limit=1] run particle minecraft:electric_spark ~ ~1.2 ~ 0.3 0.5 0.3 0.05 2
scoreboard players add #hwSparkAt itv 10
scoreboard players operation #hwSparkAt itv < #hwCritEnd itv
