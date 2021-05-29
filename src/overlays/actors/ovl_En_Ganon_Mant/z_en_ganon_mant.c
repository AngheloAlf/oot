#include "z_en_ganon_mant.h"

#define FLAGS 0x00000030

#define THIS ((EnGanonMant*)thisx)

void EnGanonMant_Init(Actor* thisx, GameState* state);
void EnGanonMant_Destroy(Actor* thisx, GameState* state);
void EnGanonMant_Update(Actor* thisx, GameState* state);
void EnGanonMant_Draw(Actor* thisx, GameState* state);

/*
const ActorInit En_Ganon_Mant_InitVars = {
    ACTOR_EN_GANON_MANT,
    ACTORCAT_BOSS,
    FLAGS,
    OBJECT_GAMEPLAY_KEEP,
    sizeof(EnGanonMant),
    (ActorFunc)EnGanonMant_Init,
    (ActorFunc)EnGanonMant_Destroy,
    (ActorFunc)EnGanonMant_Update,
    (ActorFunc)EnGanonMant_Draw,
};
*/
#pragma GLOBAL_ASM("asm/non_matchings/overlays/actors/ovl_En_Ganon_Mant/EnGanonMant_Init.s")

#pragma GLOBAL_ASM("asm/non_matchings/overlays/actors/ovl_En_Ganon_Mant/EnGanonMant_Destroy.s")

#pragma GLOBAL_ASM("asm/non_matchings/overlays/actors/ovl_En_Ganon_Mant/func_80A23D84.s")

#pragma GLOBAL_ASM("asm/non_matchings/overlays/actors/ovl_En_Ganon_Mant/func_80A23FE0.s")

#pragma GLOBAL_ASM("asm/non_matchings/overlays/actors/ovl_En_Ganon_Mant/func_80A245A4.s")

#pragma GLOBAL_ASM("asm/non_matchings/overlays/actors/ovl_En_Ganon_Mant/EnGanonMant_Update.s")

#pragma GLOBAL_ASM("asm/non_matchings/overlays/actors/ovl_En_Ganon_Mant/func_80A24884.s")

#pragma GLOBAL_ASM("asm/non_matchings/overlays/actors/ovl_En_Ganon_Mant/EnGanonMant_Draw.s")
