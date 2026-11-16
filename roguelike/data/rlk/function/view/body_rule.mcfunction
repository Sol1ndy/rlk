# round X (x_brief 판정 1, 몸의 규칙): 걷기로는 몸의 규칙을 지키는 몸(태그 rlk_bodyr: 홍련) 1.4칸 안으로 들어가지 않는다 (@s = 아바타, at @s;
# view/move 가 이번 틱의 걷기 속도 #mx · #mz view(칸/틱 × 10000)를 아바타의 Motion 에 넣기 바로 전, 그 몸이 2.2칸 안에 있을 때). 가장 가까운
# 그 몸에서 아바타 쪽으로의 단위 방향을 구해, 속도 가운데 그 몸 쪽으로 향하는 몫이 (거리 − 1.4칸)보다 크면 넘는 만큼 뺀다(옆으로 · 뒤로는
# 그대로). 박자가 세계를 멈춘 틱에도 돈다(그녀 쪽의 밀어내기 boss/scarlet/core/sep 는 그 틱에 돌지 않는다)
execute store result score #brx view run data get entity @s Pos[0] 1000
execute store result score #brz view run data get entity @s Pos[2] 1000
execute store result score #bhx view run data get entity @e[tag=rlk_bodyr,sort=nearest,limit=1] Pos[0] 1000
execute store result score #bhz view run data get entity @e[tag=rlk_bodyr,sort=nearest,limit=1] Pos[2] 1000
# 그 몸이 미끄러져 움직이는 중이면 이번 틱에 갈 자리(player/body_next: 걷기는 그녀가 옮겨진 뒤의 물리에서 적용된다). 박자가 세계를 멈춘 틱엔 그대로
execute unless score #btHold cb matches 1 as @e[tag=rlk_bodyr,sort=nearest,limit=1] if entity @s[tag=rlk_mb_mv] if score @s mbMvN matches 1.. run function rlk:player/body_next
execute unless score #btHold cb matches 1 as @e[tag=rlk_bodyr,sort=nearest,limit=1] if entity @s[tag=rlk_mb_mv] if score @s mbMvN matches 1.. run scoreboard players operation #bhx view = #bhx tmp
execute unless score #btHold cb matches 1 as @e[tag=rlk_bodyr,sort=nearest,limit=1] if entity @s[tag=rlk_mb_mv] if score @s mbMvN matches 1.. run scoreboard players operation #bhz view = #bhz tmp
scoreboard players operation #brx view -= #bhx view
scoreboard players operation #brz view -= #bhz view
execute unless score #brx view matches -2500..2500 run return 0
execute unless score #brz view matches -2500..2500 run return 0
scoreboard players operation #brn view = #brx view
scoreboard players operation #brn view *= #brx view
scoreboard players operation #brk view = #brz view
scoreboard players operation #brk view *= #brz view
scoreboard players operation #brn view += #brk view
# 1.75칸 밖이면 이번 틱의 걷기(달리기 0.28칸/틱 이하)로는 1.4칸 안에 들 수 없다
execute if score #brn view matches 3062500.. run return 0
execute if score #brn view matches ..9999 run return 0
function rlk:view/body_sqrt
scoreboard players operation #brux view = #brx view
scoreboard players operation #brux view *= #1000 tmp
scoreboard players operation #brux view /= #brd view
scoreboard players operation #bruz view = #brz view
scoreboard players operation #bruz view *= #1000 tmp
scoreboard players operation #bruz view /= #brd view
# 그 몸 쪽으로의 속도(칸/틱 × 10000) = −(속도 · 단위) / 1000, 허용 = (거리 − 1410 mb) × 10 (규칙 + 정수로 읽는 자리의 여유 0.01칸)
scoreboard players operation #brin view = #mx view
scoreboard players operation #brin view *= #brux view
scoreboard players operation #brk view = #mz view
scoreboard players operation #brk view *= #bruz view
scoreboard players operation #brin view += #brk view
scoreboard players operation #brin view /= #1000 tmp
scoreboard players operation #brin view *= #neg1 tmp
scoreboard players operation #bral view = #brd view
scoreboard players remove #bral view 1410
scoreboard players operation #bral view *= #10 tmp
execute if score #bral view matches ..-1 run scoreboard players set #bral view 0
execute if score #brin view <= #bral view run return 0
scoreboard players operation #brin view -= #bral view
scoreboard players operation #brk view = #brux view
scoreboard players operation #brk view *= #brin view
scoreboard players operation #brk view /= #1000 tmp
scoreboard players operation #mx view += #brk view
scoreboard players operation #brk view = #bruz view
scoreboard players operation #brk view *= #brin view
scoreboard players operation #brk view /= #1000 tmp
scoreboard players operation #mz view += #brk view
