# 퍼펙트 패링의 별빛, 2틱(접점): 한 번에 다 큰 크기(1.3칸 ≈ 몸 높이의 0.7), 멈춘 동안 그대로. 밝고 긴 울림(round W): 모루 둘(제 높이 =
# 무거운 종 1.27 kHz, 2배 = 2.55 kHz) + "딩" 둘(3.29 · 2.63 kHz) + 차임 셋(0.5 · 0.67 · 0.84배 = 1.98 · 2.65 · 3.32 kHz: 원작 울림의 부분음
# 1.97 · 2.6 · 3.26 kHz 자리, 0.9초까지 남는 꼬리). 예전의 자수정 울림 · 차임 · 종은 파일 음량이 낮아(차임 0.2) 거의 들리지 않았다
function rlk:player/def/fx/g/star {s:1.1}
particle minecraft:end_rod ~ ~ ~ 0.05 0.05 0.05 0.02 4 force @a[tag=player]
playsound minecraft:block.anvil.land player @a[tag=player] ~ ~ ~ 1.8 1
playsound minecraft:block.anvil.land player @a[tag=player] ~ ~ ~ 1.2 2
playsound minecraft:entity.arrow.hit_player player @a[tag=player] ~ ~ ~ 0.6 1.3
playsound minecraft:entity.arrow.hit_player player @a[tag=player] ~ ~ ~ 0.5 1.04
playsound minecraft:block.note_block.chime player @a[tag=player] ~ ~ ~ 1 0.5
playsound minecraft:block.note_block.chime player @a[tag=player] ~ ~ ~ 1 0.67
playsound minecraft:block.note_block.chime player @a[tag=player] ~ ~ ~ 1 0.84
