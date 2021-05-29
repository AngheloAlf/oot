/*
 * File: z_door_toki.c
 * Overlay: ovl_Door_Toki
 * Description: Door of Time Collision
 */

#include "z_door_toki.h"

#define FLAGS 0x00000000

#define THIS ((DoorToki*)thisx)

void DoorToki_Init(Actor* thisx, GameState* state);
void DoorToki_Destroy(Actor* thisx, GameState* state);
void DoorToki_Update(Actor* thisx, GameState* state);

const ActorInit Door_Toki_InitVars = {
    ACTOR_DOOR_TOKI,
    ACTORCAT_BG,
    FLAGS,
    OBJECT_TOKI_OBJECTS,
    sizeof(DoorToki),
    (ActorFunc)DoorToki_Init,
    (ActorFunc)DoorToki_Destroy,
    (ActorFunc)DoorToki_Update,
    NULL,
};

extern CollisionHeader D_06007888;

static InitChainEntry sInitChain[] = {
    ICHAIN_VEC3F_DIV1000(scale, 1000, ICHAIN_STOP),
};

void DoorToki_Init(Actor* thisx, GameState* state) {
    s32 pad;
    DoorToki* this = THIS;
    CollisionHeader* colHeader = NULL;

    Actor_ProcessInitChain(&this->dyna.actor, sInitChain);
    DynaPolyActor_Init(&this->dyna, DPM_UNK);
    CollisionHeader_GetVirtual(&D_06007888, &colHeader);
    this->dyna.bgId = DynaPoly_SetBgActor(globalCtx, &globalCtx->colCtx.dyna, &this->dyna.actor, colHeader);
}

void DoorToki_Destroy(Actor* thisx, GameState* state) {
    DoorToki* this = THIS;

    DynaPoly_DeleteBgActor(globalCtx, &globalCtx->colCtx.dyna, this->dyna.bgId);
}

void DoorToki_Update(Actor* thisx, GameState* state) {
    DoorToki* this = THIS;

    if (gSaveContext.eventChkInf[4] & 0x800) {
        func_8003EBF8(globalCtx, &globalCtx->colCtx.dyna, this->dyna.bgId);
    } else {
        func_8003EC50(globalCtx, &globalCtx->colCtx.dyna, this->dyna.bgId);
    }
}
