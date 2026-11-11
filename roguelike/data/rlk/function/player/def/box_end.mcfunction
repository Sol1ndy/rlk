# 퍼펙트 닷지 창이 끝났다(rlk:tick: #dgBox cb 1 이고 지금 >= #dgKill): 시작한 자리의 상자(rlk_dgo)를 지운다. 그 틱에 지우지 못했으면
# (rlk:tick 이 그 틱에 일찍 끝남 · 상자의 청크가 안 불림 · 서버가 창 안에서 멈춤) 지울 때까지 매 틱 다시 하고, 200틱 뒤에는 그만둔다
# (남은 상자는 다음 닷지가 지움; 창 밖에서는 아무도 읽지 않는다)
execute store result score #t cb run kill @e[tag=rlk_dgo]
execute if score #t cb matches 1.. run scoreboard players set #dgBox cb 0
scoreboard players operation #t cb = #now cb
scoreboard players operation #t cb -= #dgKill cb
execute if score #t cb matches 200.. run scoreboard players set #dgBox cb 0
