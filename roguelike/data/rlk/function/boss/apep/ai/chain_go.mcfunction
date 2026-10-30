# A chain is pending (plan 7.4: Q5 -> Q1 40 %, Q3 -> Q3s 30 %): it runs now (#apChainRun 1: no chain after it).
scoreboard players operation #apPick mb = #apChP mb
scoreboard players set #apChP mb 0
scoreboard players set #apChainRun mb 1
scoreboard players set #apArg mb 0
function rlk:boss/apep/ai/go_raw
