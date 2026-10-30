# @s = 플레이어, 위치 = 맞은 몹. 협동 공격을 이 자리에 예약(이번 틱의 피해 계산이 끝난 뒤 items/hook/tick_world 에서 발동)
scoreboard players operation @s eyeCd = #eyeCdT tmp
summon minecraft:marker ~ ~ ~ {Tags:["rlk_eyeq"]}
