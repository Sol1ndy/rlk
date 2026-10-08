# 데미지 텍스트 수명/애니메이션 처리

# 나이 증가
scoreboard players add @e[tag=dmgText] life 1

# 위로 천천히 떠오름
execute as @e[tag=dmgText] at @s run tp @s ~ ~0.12 ~

# 16틱(0.8초) 후 제거
kill @e[tag=dmgText,scores={life=16..}]
