# 1인칭 총구 효과 (@s = 플레이어, char/navia/fire 에서). 위치 = 블록 우산총의 축(눈 기준 오른쪽 아래, gun_spawn 과 같음), 회전 = 시선
# 우산총 끝(앞 약 1.7칸)에서 터지고 시선 높낮이를 따른다. 화면을 가리지 않게 숄더뷰보다 작다.
particle minecraft:explosion ^ ^ ^1.9 0 0 0 0 1
function rlk:fx/nv/card {kind:"burst",pos:"^ ^ ^2.0",rot:"~ ~",bb:"center",roll:12,spin:18,s0:0.5,s1:1.6,move:"0f,0f,0f",life:5,fade:2}
function rlk:fx/nv/card {kind:"glow",pos:"^ ^ ^2.15",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.4,s1:1.1,move:"0f,0f,0f",life:6,fade:3}
particle minecraft:wax_on ^ ^ ^2.1 0.4 0.4 0.4 0 16
function rlk:fx/nv/card {kind:"ring",pos:"^ ^ ^3.4",rot:"~ ~",bb:"fixed",roll:0,spin:60,s0:1.0,s1:2.6,move:"0f,0f,0f",life:6,fade:2}
