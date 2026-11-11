# @s = 플레이어. 패링 · 닷지 상태를 비운다: 시각 도장을 먼 과거로. 부르는 곳: player/init(새 플레이어 · 리셋), load(접속 중인 옛 저장),
# player/f_key · player/def/dodge_stamp · player/def/judge(도장이 없는 플레이어의 첫 입력 · 첫 피격). 도장은 게임 시각이라 런 시작 ·
# 사망 · 부활 때는 비울 필요가 없다
scoreboard players set @s parAt -1000000
scoreboard players set @s parLk -1000000
scoreboard players set @s parHit -1000000
scoreboard players set @s dgAt -1000000
scoreboard players set @s dgRw -1000000
scoreboard players set #dgEnd cb -1000000
scoreboard players set #dgKill cb -1000000
scoreboard players set #parWs cb 0
scoreboard players set #parMl cb -1000000
scoreboard players set #dgRf cb -1000000
