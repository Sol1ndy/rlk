# 중력의 물결 시작 (@s = 플레이어): 다시 쓰면 시간만 갱신(쌓인 중력은 그대로)
scoreboard players operation #cgRipT itv = #cgRipDur tmp
playsound minecraft:block.conduit.activate master @a ~ ~ ~ 0.7 1.4
playsound minecraft:block.amethyst_block.resonate master @a ~ ~ ~ 0.8 0.7
