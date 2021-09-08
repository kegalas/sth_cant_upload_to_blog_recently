;haribote-ipl
;tab=4

CYLS    equ     10  ;声明CYLS等于10

    org 0x7c00      ;指明程序装载位置

    jmp entry
    DB  0x90
    DB  "HARIBOTE"  ;启动扇区名称（8字节）
    DW  512         ;每个扇区的大小（必须512字节）
    DB  1           ;簇大小（必须为一个扇区）
    DW  1           ;fat起始位置（一般为第一个扇区）
    DB  2           ;fat个数（必须为2）
    DW  224         ;根目录大小（一般为224项）
    DW  2880        ;该磁盘大小（必须为2880扇区（对于软盘））
    DB  0xf0        ;磁盘类型（必须为0xf0）
    DW  9           ;fat的长度（必须为9扇区）
    DW  18          ;一个磁道有几个扇区（必须为18）
    DW  2           ;磁头数（必须为2）
    DD  0           ;不使用分区，必须为0
    DD  2880        ;重写一次磁盘大小
    DB  0,0,0x29    ;意义不明（但固定）
    DD  0xffffffff  ;可能是卷标号码
    DB  "HARIBOTEOS "   ;磁盘名称，必须为十一字节，不足填空格
    DB  "FAT12   "      ;磁盘格式名称，必须为八字节
    times 18 db 0      ;空18字节

;程序主体

entry:
    mov    ax,0     ;初始化寄存器
    mov    ss,ax
    mov    sp,0x7c00
    mov    ds,ax
;读取磁盘

    mov ax,0x0820
    mov es,ax
    mov ch,0    ;柱面0
    mov dh,0    ;磁头0
    mov cl,2    ;扇区2
readloop:
    mov si,0    ;记录失败次数的寄存器
retry:
    mov ah,0x02     ;读入磁盘
    mov al,1        ;一个扇区
    mov bx,0        
    mov dl,0x00     ;A驱动器
    int 0x13        ;调用磁盘bios
    jnc next        ;没出错就跳转
    add si,1        ;si累加1
    cmp si,5        ;比较si与5
    jae error       ;si>=时跳转到error
    mov ah,0x00     
    mov dl,0x00     ;A驱动器
    int 0x13        ;重置驱动器
    jmp retry

next:
    mov ax,es       ;内存地址后移0x200
    add ax,0x0020   
    mov es,ax       ;表示add ex,0x020
    add cl,1        ;cl+1
    cmp cl,18       ;比较cl和18
    jbe readloop    ;cl<=18跳转到readloop
    mov cl,1
    add dh,1
    cmp dh,2
    jb  readloop    ;dh<2跳转到readloop
    mov dh,0
    add ch,1
    cmp ch,CYLS
    jb  readloop    ;ch<CYLS跳转到readloop
;读取结束,跳转到haribote.sys
    
    mov [0x0ff0],ch     ;记录ipl读到哪里了
    jmp 0xc200


error:
    mov SI,msg
putloop:
    mov al,[si]
    add si,1    ;给si加1
    cmp al,0
    je  fin
    mov ah,0x0e ;显示一个文字
    mov bx,15   ;指定字符颜色
    int 0x10    ;调用显卡bios
    jmp putloop

fin:
    hlt     ;让cpu停止，等待指令
    jmp fin ;无限循环

msg:
    DB 0x0a,0x0a        ;换行两次
    DB "load error"
    DB 0x0a             ;换行
    DB 0

    times 510-($-$$)    db 0    ;填写0x00直到0x001fe

    DB 0x55,0xaa

