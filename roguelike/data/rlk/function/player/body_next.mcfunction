# round X (몸의 규칙): @s = 몸의 규칙을 지키는 몸(rlk_bodyr: 홍련)이 미끄러져 움직이는 중(rlk_mb_mv). 이번 틱에 그 몸이 갈 자리(mboss/mv/tick 이
# 이 플레이어 쪽 줄들 뒤에, 같은 계산으로 옮겨 놓을 자리: mbMvT + 1)를 #bhx · #bhz tmp(칸 × 1000)에. 플레이어의 걷기(view/body_rule) · 닷지
# (player/dodge/body)는 그녀가 이번 틱에 설 자리에 대해 몸의 규칙을 지킨다
scoreboard players operation #bnt tmp = @s mbMvT
scoreboard players add #bnt tmp 1
scoreboard players operation #bhx tmp = @s mbMvX1
scoreboard players operation #bhx tmp -= @s mbMvX0
scoreboard players operation #bhx tmp *= #bnt tmp
scoreboard players operation #bhx tmp /= @s mbMvN
scoreboard players operation #bhx tmp += @s mbMvX0
scoreboard players operation #bhz tmp = @s mbMvZ1
scoreboard players operation #bhz tmp -= @s mbMvZ0
scoreboard players operation #bhz tmp *= #bnt tmp
scoreboard players operation #bhz tmp /= @s mbMvN
scoreboard players operation #bhz tmp += @s mbMvZ0
