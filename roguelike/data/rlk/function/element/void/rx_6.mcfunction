# 진공 (공허+바람): 반경 3칸의 다른 적에게 대상 잠식의 40% 를 더해 주고 공허 부착 + 바람 피해 60%
function rlk:element/calc {m:60}
scoreboard players set @s rxQ 22
scoreboard players operation @s rxDmg = #rdmg tmp
scoreboard players set @s rxEl 6
