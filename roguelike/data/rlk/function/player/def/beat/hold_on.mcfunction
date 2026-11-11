# 세계가 멈추는 틱: 스스로 걷는 몹(rlk_mob 가운데 NoAI 가 아닌 것: 바닐라 몹 · 커스텀 몹의 두뇌)을 NoAI 로 세운다(표식 rlk_bt_noai).
# 이미 NoAI 인 몹(빙결 · 그로기 · 보스 몸 · 원래 NoAI)은 건드리지 않는다
scoreboard players set #btHeld cb 1
execute as @e[tag=rlk_mob,tag=!rlk_bt_noai] unless data entity @s {NoAI:1b} run function rlk:player/def/beat/mob_hold
