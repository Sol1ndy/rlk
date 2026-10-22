# (매크로 boss_id) 그 보스의 문 표시 저장소가 있으면 문 오브젝트를 세운다. oarg = 레지스트리 번호 n
# 저장소가 없어도(prep이 돌지 않았거나 실패, 저장소가 지워짐) 문은 꼭 세운다(문이 없는 보스 맵 = 진행 불가): 레지스트리의 문 기록으로
$execute unless data storage rlk:mboss cprep.$(boss_id).gate run return run function rlk:room/obj/k_cboss_fb with storage rlk:mboss cbyid.$(boss_id)
scoreboard players set #oact tmp 16
$execute store result score #oarg tmp run data get storage rlk:mboss cprep.$(boss_id).gate.n
$function rlk:room/obj/k_cboss3 with storage rlk:mboss cprep.$(boss_id).gate
