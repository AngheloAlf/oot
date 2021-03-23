#ifndef _NES_MSG_MACROS_H_ // Maybe something like _Z64_NES_MSG_H_ // and rename file accordingly
#define _NES_MSG_MACROS_H_

#define MSG_COLOR_DEFAULT       "\x40"
// White, apart from Type 5 boxes, for which Black

#define MSG_COLOR_RED           "\x41"
#define MSG_COLOR_GREEN         "\x42"
#define MSG_COLOR_BLUE          "\x43"
#define MSG_COLOR_LIGHTBLUE     "\x44"
#define MSG_COLOR_PINK          "\x45"
#define MSG_COLOR_YELLOW        "\x46"
#define MSG_COLOR_WHITE         "\x47"

#define MSG_COLOR_EXPAND0(color)  color
#define MSG_COLOR_EXPAND1(color)  MSG_COLOR_EXPAND0(color)
#define MSG_COLOR(color)  MSG_COLOR_EXPAND1(MSG_COLOR_##color)

//#define MSGCODE_TEXTCOLOR(color) "\x00\x0B" MSG_COLOR(color)


#define MSGCODE_LINEBREAK "\x01"
#define MSGCODE_ENDMARKER "\x02"
#define MSGCODE_BOXBREAK "\x04"
#define MSGCODE_TEXTCOLOR(color) "\x05" MSG_COLOR(color) // "\x00\x0B" "\x0C" MSG_COLOR(color)
#define MSGCODE_INDENT(space) "\x06" space //
#define MSGCODE_NEXTMSGID(x, y) "\x07" x y //
#define MSGCODE_INSTANT_ON "\x08"
#define MSGCODE_INSTANT_OFF "\x09"
#define MSGCODE_KEEPOPEN "\x0A"
#define MSGCODE_UNKEVENT "\x0B"
#define MSGCODE_DELAY_BOXBREAK(x) "\x0C" x //
#define MSGCODE_UNUSED_1 "\x0D"
#define MSGCODE_DELAY_FADEOUT(x) "\x0E" x //
#define MSGCODE_PLAYERNAME "\x0F"
#define MSGCODE_BEGINOCARINA "\x10"
#define MSGCODE_UNUSED_2 "\x11"
#define MSGCODE_PLAYSOUND(x, y) "\x12" x y
#define MSGCODE_ITEMICON(x) "\x13" x //
#define MSGCODE_TEXTSPEED(x) "\x14" x //
#define MSGCODE_BACKGROUND(x, y, z) "\x15" x y z
#define MSGCODE_MARATHONTIME "\x16"
#define MSGCODE_HORSERACETIME "\x17"
#define MSGCODE_HORSEBACKARCHERYSCORE "\x18"
#define MSGCODE_GOLDSKULLTULATOTAL "\x19"
#define MSGCODE_NOSKIP "\x1A"
#define MSGCODE_TWOCHOICE "\x1B"
#define MSGCODE_THREECHOICE "\x1C"
#define MSGCODE_FISHSIZE "\x1D"
#define MSGCODE_HIGHSCORE(x) "\x1E" x //
#define MSGCODE_TIME "\x1F"


// Special characters

#define MSGCODE_E_ACUTE_LOWERCASE "\x96" // "é"


#define MSGCODE_A_BTN "\x9F"
#define MSGCODE_B_BTN "\xA0"
#define MSGCODE_C_BTN "\xA1"
#define MSGCODE_L_BTN "\xA2"
#define MSGCODE_R_BTN "\xA3"
#define MSGCODE_Z_BTN "\xA4"
#define MSGCODE_CUP_BTN "\xA5"
#define MSGCODE_CDOWN_BTN "\xA6"
#define MSGCODE_CLEFT_BTN "\xA7"
#define MSGCODE_CRIGHT_BTN "\xA8"
#define MSGCODE_TARGET_ICON "\xA9"
#define MSGCODE_STICK "\xAA"
#define MSGCODE_DPAD "\xAB"


#endif
