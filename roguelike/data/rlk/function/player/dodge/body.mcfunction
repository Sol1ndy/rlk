# round X (x_brief 판정 1, 몸의 규칙): 닷지의 모든 동작(비틀기 · 내딛는 걸음 · 백스텝 · 옆돌기)은 몸의 규칙을 지키는 몸(태그 rlk_bodyr:
# 홍련) 앞에서 멈춘다 (@s = 플레이어, player/dash_move_tick; 그 몸이 아바타 3칸 안이거나 미끄러져 움직이는 중). 이번 틱의 이동(#dgSp 를 dashUX · dashUZ 쪽으로)이 끝나는
# 자리가 그 몸에서 1.4칸 안이고 그 몸 쪽으로 가는 이동이면, 이번 틱은 움직이지 않고 동작을 끝낸다(player/dodge/stop). 옆으로 · 멀어지는
# 쪽은 그대로(그 몸에 붙어 있어도 빠져나갈 수 있다)
# 이번 틱의 이동(칸 × 1000) = 단위 × 100 × #dgSp / 100
scoreboard players operation #bqx tmp = @s dashUX
scoreboard players operation #bqx tmp *= #dgSp tmp
scoreboard players operation #bqx tmp /= #100 tmp
scoreboard players operation #bqz tmp = @s dashUZ
scoreboard players operation #bqz tmp *= #dgSp tmp
scoreboard players operation #bqz tmp /= #100 tmp
# 아바타 · 가장 가까운 그 몸(칸 × 1000)
execute store result score #bax tmp run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000
execute store result score #baz tmp run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000
execute at @e[tag=rlk_body,limit=1] store result score #bhx tmp run data get entity @e[tag=rlk_bodyr,sort=nearest,limit=1] Pos[0] 1000
execute at @e[tag=rlk_body,limit=1] store result score #bhz tmp run data get entity @e[tag=rlk_bodyr,sort=nearest,limit=1] Pos[2] 1000
# 그 몸이 미끄러져 움직이는 중이면 이번 틱에 갈 자리(player/body_next; mboss/mv/tick 은 이 줄 뒤에 그녀를 옮긴다). 박자가 세계를 멈춘 틱엔 그대로
execute unless score #btHold cb matches 1 at @e[tag=rlk_body,limit=1] as @e[tag=rlk_bodyr,sort=nearest,limit=1] if entity @s[tag=rlk_mb_mv] if score @s mbMvN matches 1.. run function rlk:player/body_next
scoreboard players operation #bhx tmp -= #bax tmp
scoreboard players operation #bhz tmp -= #baz tmp
# 그 몸 쪽으로 가는가: (그 몸 − 아바타) · 이동 > 0
scoreboard players operation #bdt tmp = #bhx tmp
scoreboard players operation #bdt tmp *= #bqx tmp
scoreboard players operation #bkk tmp = #bhz tmp
scoreboard players operation #bkk tmp *= #bqz tmp
scoreboard players operation #bdt tmp += #bkk tmp
execute if score #bdt tmp matches ..0 run return 0
# 끝나는 자리에서 그 몸까지(칸 × 1000)의 제곱 < 1.41² × 10⁶ (규칙 1.4칸 + 정수로 읽는 자리의 여유 0.01칸)
scoreboard players operation #bhx tmp -= #bqx tmp
scoreboard players operation #bhz tmp -= #bqz tmp
execute unless score #bhx tmp matches -3000..3000 run return 0
execute unless score #bhz tmp matches -3000..3000 run return 0
scoreboard players operation #bdt tmp = #bhx tmp
scoreboard players operation #bdt tmp *= #bhx tmp
scoreboard players operation #bkk tmp = #bhz tmp
scoreboard players operation #bkk tmp *= #bhz tmp
scoreboard players operation #bdt tmp += #bkk tmp
execute if score #bdt tmp matches ..1988099 run function rlk:player/dodge/stop
