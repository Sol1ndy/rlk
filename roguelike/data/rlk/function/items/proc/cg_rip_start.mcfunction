# 중력의 물결 시작 (@s = 플레이어): 다시 쓰면 시간만 갱신(쌓인 중력은 그대로)
scoreboard players operation #cgRipT itv = #cgRipDur tmp
execute unless score #k187 snd matches 1 run function rlk:snd/f202
execute unless score #k188 snd matches 1 run function rlk:snd/f203
