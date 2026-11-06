# 결정 가시 장미 (@s = 플레이어, char/navia/muzzle_rig 에서: 위치 = 우산 축, 회전 = 발사 방향 + 시선 높낮이)
# v4 FX7: 길고 가는 마름모꼴 금빛 결정 가시가 우산 끝 약 1칸 앞(펼친 덮개 너머) 한 점에서 앞쪽 부채꼴(약 120도)로 뻗어 나가 8틱쯤 남는다.
# 카드 면은 발사 방향을 향하고(뒤의 숄더뷰 카메라에서 보이게), 둘은 좌우로 30도 틀어 앞쪽으로 기울어 보이게 한다.
function rlk:fx/nv/card {kind:"shard",pos:"^ ^ ^2.1",rot:"~ ~",bb:"fixed",roll:-150,spin:0,s0:0,s1:1.2,move:"0f,0f,0f",life:8,fade:3}
function rlk:fx/nv/card {kind:"shard",pos:"^ ^ ^2.1",rot:"~30 ~",bb:"fixed",roll:-75,spin:0,s0:0,s1:1.7,move:"0f,0f,0f",life:9,fade:3}
function rlk:fx/nv/card {kind:"shard",pos:"^ ^ ^2.1",rot:"~ ~",bb:"fixed",roll:-15,spin:0,s0:0,s1:1.5,move:"0f,0f,0f",life:8,fade:3}
function rlk:fx/nv/card {kind:"shard",pos:"^ ^ ^2.1",rot:"~-30 ~",bb:"fixed",roll:55,spin:0,s0:0,s1:1.8,move:"0f,0f,0f",life:9,fade:3}
function rlk:fx/nv/card {kind:"shard",pos:"^ ^ ^2.1",rot:"~ ~",bb:"fixed",roll:125,spin:0,s0:0,s1:1.1,move:"0f,0f,0f",life:8,fade:3}
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.7} ^ ^ ^2.2 0.4 0.4 0.2 0 8 normal
