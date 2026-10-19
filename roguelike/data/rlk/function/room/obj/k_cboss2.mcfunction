# (매크로 boss_id) 그 보스의 문 표시 저장소가 있으면 문 오브젝트를 세운다. oarg = 레지스트리 번호 n
$execute unless data storage rlk:mboss cprep.$(boss_id).gate run return 0
scoreboard players set #oact tmp 16
$execute store result score #oarg tmp run data get storage rlk:mboss cprep.$(boss_id).gate.n
$function rlk:room/obj/k_cboss3 with storage rlk:mboss cprep.$(boss_id).gate
