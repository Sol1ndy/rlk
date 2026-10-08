# 곧 꺼질 여광 (@s = 플레이어, at 몸): 생명의 계약 +#clBurstBol%, 그 뒤 앞쪽 범위를 5번 베어 번개 원소 범위 피해(참격당 127%)
scoreboard players operation #bolPct tmp = #clBurstBol tmp
function rlk:player/bol/add_pct
scoreboard players set @s clBurst 1
kill @e[tag=rlk_clb]
execute rotated ~ 0 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_clb"]}
execute rotated ~ 0 run tp @e[tag=rlk_clb] ~ ~ ~ ~ ~
playsound minecraft:entity.lightning_bolt.thunder master @a ~ ~ ~ 0.4 1.6
playsound minecraft:item.trident.thunder master @a ~ ~ ~ 0.5 1.7
