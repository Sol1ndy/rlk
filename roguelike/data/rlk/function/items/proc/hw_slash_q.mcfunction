# 「홍련일섬」 시전 (@s = 플레이어, 위치 · 방향 = 몸, items/hook/on_cast_burst: 원소폭발을 쓴 순간, 재사용 대기가 아닐 때)
# 재사용 대기(#hwSlCd 1, #hwSlEnd = 지금 + #hwSlCdT) · 지금 + #hwSlDelay 틱에 베기(#hwSlAt, hw_slash)
# · 시전 때 체력이 최대 체력의 #hwSlHp % 이하이면 #hwSlCritDur 틱 동안 치명타 확률 +(#hwCritT 1, #hwCritEnd)
scoreboard players set #hwOn itv 1
execute store result score #hwNow itv run time query gametime
scoreboard players set #hwSlCd itv 1
scoreboard players operation #hwSlEnd itv = #hwNow itv
scoreboard players operation #hwSlEnd itv += #hwSlCdT tmp
scoreboard players set #hwSlQ itv 1
scoreboard players operation #hwSlAt itv = #hwNow itv
scoreboard players operation #hwSlAt itv += #hwSlDelay tmp
scoreboard players operation #hwNext itv < #hwSlAt itv
scoreboard players operation #hwWait itv < #hwSlDelay tmp
scoreboard players operation #hwA itv = @s curHealth
scoreboard players operation #hwA itv *= #100 tmp
scoreboard players operation #hwB itv = @s maxHealth
scoreboard players operation #hwB itv *= #hwSlHp tmp
scoreboard players set #hwCritT itv 0
execute if score #hwA itv <= #hwB itv run scoreboard players set #hwCritT itv 1
scoreboard players operation #hwCritEnd itv = #hwNow itv
scoreboard players operation #hwCritEnd itv += #hwSlCritDur tmp
scoreboard players operation #hwSparkAt itv = #hwNow itv
scoreboard players add #hwSparkAt itv 10
scoreboard players operation #hwSparkAt itv < #hwCritEnd itv
# 신호: 숨을 들이쉬는 바람 소리 · 몸 둘레 보랏빛 고리(반지름 2칸) · 화면 가장자리 어둠 6틱(글리프 vig). 어둠은 큰 제목(vBig)이나
# 아랫줄 글(ttlT: 대사 · 안내)이 떠 있으면 생략(제목 시간을 바꾸면 그 글이 일찍 사라지므로)
execute unless score #k356 snd matches 1 run function rlk:snd/f426
particle minecraft:dust{color:[0.79f,0.63f,1.0f],scale:1.2f} ~2 ~0.2 ~ 0 0 0 0 1
particle minecraft:dust{color:[0.79f,0.63f,1.0f],scale:1.2f} ~1.732 ~0.2 ~1 0 0 0 0 1
particle minecraft:dust{color:[0.79f,0.63f,1.0f],scale:1.2f} ~1 ~0.2 ~1.732 0 0 0 0 1
particle minecraft:dust{color:[0.79f,0.63f,1.0f],scale:1.2f} ~ ~0.2 ~2 0 0 0 0 1
particle minecraft:dust{color:[0.79f,0.63f,1.0f],scale:1.2f} ~-1 ~0.2 ~1.732 0 0 0 0 1
particle minecraft:dust{color:[0.79f,0.63f,1.0f],scale:1.2f} ~-1.732 ~0.2 ~1 0 0 0 0 1
particle minecraft:dust{color:[0.79f,0.63f,1.0f],scale:1.2f} ~-2 ~0.2 ~ 0 0 0 0 1
particle minecraft:dust{color:[0.79f,0.63f,1.0f],scale:1.2f} ~-1.732 ~0.2 ~-1 0 0 0 0 1
particle minecraft:dust{color:[0.79f,0.63f,1.0f],scale:1.2f} ~-1 ~0.2 ~-1.732 0 0 0 0 1
particle minecraft:dust{color:[0.79f,0.63f,1.0f],scale:1.2f} ~ ~0.2 ~-2 0 0 0 0 1
particle minecraft:dust{color:[0.79f,0.63f,1.0f],scale:1.2f} ~1 ~0.2 ~-1.732 0 0 0 0 1
particle minecraft:dust{color:[0.79f,0.63f,1.0f],scale:1.2f} ~1.732 ~0.2 ~-1 0 0 0 0 1
execute unless score @s vBig matches 1.. unless score @s ttlT matches 1.. run title @s times 0 4 2
execute unless score @s vBig matches 1.. unless score @s ttlT matches 1.. run title @s title {text:"",extra:[{text:"",font:"rlk:mboss_hr",shadow_color:0}]}
execute unless score @s vBig matches 1.. unless score @s ttlT matches 1.. run scoreboard players set @s vBig 6
