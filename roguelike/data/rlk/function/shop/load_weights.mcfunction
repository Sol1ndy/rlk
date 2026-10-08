# macro: si. 스테이지 si의 등급 threshold를 #t1/#t2/#t3에
$execute store result score #t1 tmp run data get storage rlk:shop wt.s$(si).t1
$execute store result score #t2 tmp run data get storage rlk:shop wt.s$(si).t2
$execute store result score #t3 tmp run data get storage rlk:shop wt.s$(si).t3
