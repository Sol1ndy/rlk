# 공허 개화 (공허+풀): 붉은 꽃이 터져 반경 2칸 풀 피해 60%. 잔향은 「만개 잔향」으로 저장된다(재연하면 다음 잔향과 함께 두 발)
function rlk:element/calc {m:60}
scoreboard players set @s rxQ 23
scoreboard players operation @s rxDmg = #rdmg tmp
scoreboard players set @s rxEl 7
