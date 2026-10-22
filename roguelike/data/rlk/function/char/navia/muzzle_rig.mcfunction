# 숄더뷰 총구 효과 (@s = 플레이어, char/navia/fire 에서). 위치 = 몸 디스플레이 우산의 축(오른쪽 0.3칸, 높이 1.12), 회전 = 발사 방향 + 시선 높낮이
# 섬광 · 빛무리 · 폭발 입자는 우산 끝에 둔다(몸의 우산은 위아래로 기울지 않는다: 바로 발사 7틱 끝 ≈ 앞 1.36, 조준 후 발사 3틱 ≈ 앞 1.05~1.2).
# 원뿔 끝 고리와 반짝임은 탄이 나가는 방향(높낮이 포함)을 따른다. 큰 섬광은 펼친 덮개 둘레로 삐져나와 보인다.
execute rotated ~ 0 run particle minecraft:explosion ^ ^ ^1.45 0 0 0 0 1
execute rotated ~ 0 run function rlk:fx/nv/card {kind:"burst",pos:"^ ^ ^1.4",rot:"~ ~",bb:"center",roll:12,spin:18,s0:0.9,s1:2.8,move:"0f,0f,0f",life:5,fade:2}
execute rotated ~ 0 run function rlk:fx/nv/card {kind:"glow",pos:"^ ^ ^1.55",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.6,s1:1.8,move:"0f,0f,0f",life:6,fade:3}
particle minecraft:wax_on ^ ^ ^1.8 0.4 0.4 0.4 0 16
# 원뿔 끝 고리: 밝은 선이 반지름 약 2칸(0.43 × 4.8)까지 퍼진다(v5 FX-4)
function rlk:fx/nv/card {kind:"ring",pos:"^ ^ ^2.8",rot:"~ ~",bb:"fixed",roll:0,spin:60,s0:1.4,s1:4.8,move:"0f,0f,0f",life:6,fade:2}
# 조준 후 발사(skill_fire): 섬광 뒤 앞쪽으로 퍼지는 금빛 결정 가시 장미(v4 FX7). 시선 높낮이를 따른다
execute if data storage rlk:player_motion active{clip:"skill_fire"} run function rlk:char/navia/shard_rose
