# round X (x_brief 판정 1): 살짝 전진(player/nudge: 클로린드의 밤 꿰뚫기)은 보스의 몸(rlk_mb_body) 1.6칸 앞에서 멈춘다 (@s = 플레이어,
# player/step_move_tick; 보스 몸이 아바타 3칸 안). 이번 틱의 전진(dashDX · dashDZ, 칸 × 1000)이 끝나는 자리가 보스 몸에서 1.6칸 안이고
# 그 몸 쪽으로 가는 전진이면 여기서 끝낸다(stepT 0)
execute store result score #bax tmp run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000
execute store result score #baz tmp run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000
execute at @e[tag=rlk_body,limit=1] store result score #bhx tmp run data get entity @e[tag=rlk_mb_body,sort=nearest,limit=1] Pos[0] 1000
execute at @e[tag=rlk_body,limit=1] store result score #bhz tmp run data get entity @e[tag=rlk_mb_body,sort=nearest,limit=1] Pos[2] 1000
scoreboard players operation #bhx tmp -= #bax tmp
scoreboard players operation #bhz tmp -= #baz tmp
scoreboard players operation #bdt tmp = #bhx tmp
scoreboard players operation #bdt tmp *= @s dashDX
scoreboard players operation #bkk tmp = #bhz tmp
scoreboard players operation #bkk tmp *= @s dashDZ
scoreboard players operation #bdt tmp += #bkk tmp
execute if score #bdt tmp matches ..0 run return 0
scoreboard players operation #bhx tmp -= @s dashDX
scoreboard players operation #bhz tmp -= @s dashDZ
execute unless score #bhx tmp matches -3000..3000 run return 0
execute unless score #bhz tmp matches -3000..3000 run return 0
scoreboard players operation #bdt tmp = #bhx tmp
scoreboard players operation #bdt tmp *= #bhx tmp
scoreboard players operation #bkk tmp = #bhz tmp
scoreboard players operation #bkk tmp *= #bhz tmp
scoreboard players operation #bdt tmp += #bkk tmp
execute if score #bdt tmp matches ..2559999 run scoreboard players set @s stepT 0
