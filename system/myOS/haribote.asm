;haribote-os
;tab=4

;有关boot_info
CYLS    equ     0x0ff0      ;设定启动区
LEDS    equ     0x0ff1
VMODE   equ     0x0ff2      ;关于颜色数目的信息。颜色的位数。
SCRNX   equ     0x0ff4      ;分辨率的x
SCRNY   equ     0x0ff6      ;分辨率的y
VRAM    equ     0x0ff8      ;图像缓冲区的开始地址




    org 0xc200
    mov al,0x13     ;VGA显卡,320x200x8位彩色
    mov ah,0x00
    int 0x10
    mov byte [VMODE],8  ;记录画面模式
    mov word [SCRNX],320
    mov word [SCRNY],200
    mov DWORD [VRAM],0x000a0000

;用bios取得键盘上各种LED指示灯的状态
    mov ah,0x02
    int 0x16        ;keyboard BIOS
    mov [LEDS],al


fin:
    hlt
    jmp fin