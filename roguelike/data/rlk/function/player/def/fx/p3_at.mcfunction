# 퍼펙트 패링의 접점, 0틱: 작은 불티와 무거운 쇳소리. 소리(round W; 층마다 음량 · 높이 · 틱은 README 3 의 표): 모루(음량 2 = 파일 음량 0.5 를
# 끝까지 올림, 1.6배 = 2.04 kHz 의 울림) + 철문을 치는 소리(낮은 몸통) + 삼지창 타격(날카로운 앞머리). 불꽃놀이 "반짝"은 파일의 터짐이 0.3초
# 뒤에 오므로 여기서 틀어 6틱(풀림)의 불꽃 줄기와 맞춘다. 음량 1 초과 = 거리 감쇠만 줄어든다(카메라는 몸에서 4칸 뒤: client SoundEngine)
function rlk:player/def/fx/g/spark {s:1.3,c:"white"}
particle minecraft:crit ~ ~ ~ 0.15 0.15 0.15 0.5 8 force @a[tag=player]
particle minecraft:electric_spark ~ ~ ~ 0.08 0.08 0.08 0.4 6 force @a[tag=player]
playsound minecraft:block.anvil.land player @a[tag=player] ~ ~ ~ 2 1.6
playsound minecraft:entity.zombie.attack_iron_door player @a[tag=player] ~ ~ ~ 0.7 0.9
playsound minecraft:item.trident.hit player @a[tag=player] ~ ~ ~ 0.8 1.2
playsound minecraft:entity.firework_rocket.twinkle player @a[tag=player] ~ ~ ~ 0.5 1.4
