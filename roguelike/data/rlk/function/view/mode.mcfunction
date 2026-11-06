# 시점 종류 바꾸기: /function rlk:view/mode {m:1} (1 숄더뷰 · 2 F5 위쪽 시점). 켜져 있지 않으면 켠다  ({m:"help"}: 번호 목록)
# 매크로 함수는 통째로 해석되므로 점수 줄은 mode_do 에 둔다(m = help 여도 이 함수는 해석된다)
$data modify storage rlk:tmp hq set value "$(m)"
execute if data storage rlk:tmp {hq:"help"} run return run function rlk:view/mode_help
$function rlk:view/mode_do {m:$(m)}
