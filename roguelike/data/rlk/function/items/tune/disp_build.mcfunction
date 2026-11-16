# macro: id → 설명(abilities)의 숫자 자리표 {tk:{c,x,d,p,u}} 를 지금 상수 값으로 바꾼 사본 rlk:items disp.<id> (자리표가 없으면 만들지 않음)
# 값 = 상수 × x ÷ d, 소수 p 자리(0~2, 끝이 0 이면 생략), 뒤에 단위 u. 예: {tk:{c:"#bracerRes",x:1,d:1,p:0,u:"%"},color:"#FFE08A"}
$data remove storage rlk:items disp.$(id)
$data modify storage rlk:tune dl set from storage rlk:items registry.$(id).abilities
data modify storage rlk:tune dout set value []
scoreboard players set #dtk tmp 0
function rlk:items/tune/disp_line_loop
$execute if score #dtk tmp matches 1.. run data modify storage rlk:items disp.$(id) set from storage rlk:tune dout
