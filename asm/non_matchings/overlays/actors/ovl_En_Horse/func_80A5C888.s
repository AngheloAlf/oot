glabel func_80A5C888
/* 01598 80A5C888 27BDFFE8 */  addiu   $sp, $sp, 0xFFE8           ## $sp = FFFFFFE8
/* 0159C 80A5C88C AFBF0014 */  sw      $ra, 0x0014($sp)           
/* 015A0 80A5C890 8CA61C44 */  lw      $a2, 0x1C44($a1)           ## 00001C44
/* 015A4 80A5C894 AFA40018 */  sw      $a0, 0x0018($sp)           
/* 015A8 80A5C898 24070190 */  addiu   $a3, $zero, 0x0190         ## $a3 = 00000190
/* 015AC 80A5C89C 0C296D78 */  jal     func_80A5B5E0              
/* 015B0 80A5C8A0 24C60024 */  addiu   $a2, $a2, 0x0024           ## $a2 = 00000024
/* 015B4 80A5C8A4 8FA40018 */  lw      $a0, 0x0018($sp)           
/* 015B8 80A5C8A8 8C8E01F0 */  lw      $t6, 0x01F0($a0)           ## 000001F0
/* 015BC 80A5C8AC 31CF4000 */  andi    $t7, $t6, 0x4000           ## $t7 = 00000000
/* 015C0 80A5C8B0 51E0000D */  beql    $t7, $zero, .L80A5C8E8     
/* 015C4 80A5C8B4 84890032 */  lh      $t1, 0x0032($a0)           ## 00000032
/* 015C8 80A5C8B8 84980032 */  lh      $t8, 0x0032($a0)           ## 00000032
/* 015CC 80A5C8BC 3C014448 */  lui     $at, 0x4448                ## $at = 44480000
/* 015D0 80A5C8C0 44814000 */  mtc1    $at, $f8                   ## $f8 = 800.00
/* 015D4 80A5C8C4 44982000 */  mtc1    $t8, $f4                   ## $f4 = 0.00
/* 015D8 80A5C8C8 00000000 */  nop
/* 015DC 80A5C8CC 468021A0 */  cvt.s.w $f6, $f4                   
/* 015E0 80A5C8D0 46083280 */  add.s   $f10, $f6, $f8             
/* 015E4 80A5C8D4 4600540D */  trunc.w.s $f16, $f10                 
/* 015E8 80A5C8D8 44088000 */  mfc1    $t0, $f16                  
/* 015EC 80A5C8DC 00000000 */  nop
/* 015F0 80A5C8E0 A4880032 */  sh      $t0, 0x0032($a0)           ## 00000032
/* 015F4 80A5C8E4 84890032 */  lh      $t1, 0x0032($a0)           ## 00000032
.L80A5C8E8:
/* 015F8 80A5C8E8 A48900B6 */  sh      $t1, 0x00B6($a0)           ## 000000B6
/* 015FC 80A5C8EC 8FBF0014 */  lw      $ra, 0x0014($sp)           
/* 01600 80A5C8F0 27BD0018 */  addiu   $sp, $sp, 0x0018           ## $sp = 00000000
/* 01604 80A5C8F4 03E00008 */  jr      $ra                        
/* 01608 80A5C8F8 00000000 */  nop