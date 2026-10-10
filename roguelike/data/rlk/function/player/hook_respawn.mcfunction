# 부활 시 추가 처리 지점 (@s = 플레이어)
# 보스 테스트 중 쓰러짐: 캐릭터 초기화 없이 테스트만 끝내고 로비로
execute if score #rdTest rd matches 1 run return run function rlk:boss/raiden/test/defeat
execute if score #active room matches 1 run function rlk:run/fail
