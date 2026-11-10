# @s = 우클릭을 기록한 interaction(player/def/input). 입력 실드 · 몹 / 아바타 실드만 소비한다(다른 interaction 은 그대로)
execute if entity @s[tag=rlk_mshield] at @s run return run function rlk:combat/input/poll_right
execute if entity @s[tag=atkBlock] run return run function rlk:combat/input/poll_right
execute if entity @s[tag=atkStrike] run return run function rlk:combat/input/poll_right
