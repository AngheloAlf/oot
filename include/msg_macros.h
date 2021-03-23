
#define MSGCODE_LINEBREAK "\x00\x0A"
#define MSGCODE_ENDMARKER "\x81\x70"
#define MSGCODE_BOXBREAK "\x81\xA5"
#define MSGCODE_TEXTCOLOR(color) "\x00\x0B\x0C" color //
#define MSGCODE_INDENT(space) "\x86\xC7\x00" space //
#define MSGCODE_NEXTMSGID(x, y) "\x81\xCB" x y //
#define MSGCODE_INSTANT_ON "\x81\x89"
#define MSGCODE_INSTANT_OFF "\x81\x8A"
#define MSGCODE_KEEPOPEN "\x86\xC8"
#define MSGCODE_UNKEVENT "\x81\x9F"
#define MSGCODE_DELAY_BOXBREAK(x) "\x81\xAC\x00" x //
//#define MSGCODE_UNUSED_1
#define MSGCODE_DELAY_FADEOUT(x) "\x81\x9E\x00" x //
#define MSGCODE_PLAYERNAME "\x87\x4F"
#define MSGCODE_BEGINOCARINA "\x81\xF0"
//#define MSGCODE_UNUSED_2
#define MSGCODE_PLAYSOUND(x, y) "\x81\xF3" x y // TODO: fix
#define MSGCODE_ITEMICON(x) "\x81\x9A\x00" x //
#define MSGCODE_TEXTSPEED(x) "\x86\xC9\x00" x //
#define MSGCODE_BACKGROUND(x, y, z) "\x86\xB3\x00" x y z //
#define MSGCODE_MARATHONTIME "\x87\x91"
#define MSGCODE_HORSERACETIME "\x87\x92"
#define MSGCODE_HORSEBACKARCHERYSCORE "\x87\x9B"
#define MSGCODE_GOLDSKULLTULATOTAL "\x86\xA3"
#define MSGCODE_NOSKIP "\x81\x99"
#define MSGCODE_TWOCHOICE "\x81\xBC"
#define MSGCODE_THREECHOICE "\x81\xB8"
#define MSGCODE_FISHSIZE "\x86\xA4"
#define MSGCODE_HIGHSCORE(x) "\x86\x9F\x00" x //
#define MSGCODE_TIME "\x81\xA1"


#define MSGCODE_A_BTN "\x83\x9F"
#define MSGCODE_B_BTN "\x83\xA0"
#define MSGCODE_C_BTN "\x83\xA1"
#define MSGCODE_L_BTN "\x83\xA2"
#define MSGCODE_R_BTN "\x83\xA3"
#define MSGCODE_Z_BTN "\x83\xA4"
#define MSGCODE_CUP_BTN "\x83\xA5"
#define MSGCODE_CDOWN_BTN "\x83\xA6"
#define MSGCODE_CLEFT_BTN "\x83\xA7"
#define MSGCODE_CRIGHT_BTN "\x83\xA8"
#define MSGCODE_TARGET_ICON "\x83\xA9"
#define MSGCODE_STICK "\x83\xAA"
#define MSGCODE_DPAD "\x83\xAB"

