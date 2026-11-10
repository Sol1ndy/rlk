# 패링할 수 없는 공격의 경고 섬광 (위치 = 보스의 가슴; mboss/np_glint · fx/rd_glint): 금빛 구 고리 + 긴 가로 섬광(g/glint, 6틱),
# 노란 먼지 · 빛 줄기, 종 · 신호기 소리(글자 안내 없음)
function rlk:player/def/fx/g/glint
particle minecraft:dust{color:[1f,0.88f,0.3f],scale:1.0f} ~ ~ ~ 0.4 0.4 0.4 0 16 force @a[tag=player]
particle minecraft:end_rod ~ ~ ~ 1.2 0.04 1.2 0 8 force @a[tag=player]
playsound minecraft:block.bell.use hostile @a[tag=player] ~ ~ ~ 0.7 1.6
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.45 2
