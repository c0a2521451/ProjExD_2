import os
import sys
import random
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA={
            pg.K_UP:(0,-5),
            pg.K_DOWN:(0,5),
            pg.K_LEFT:(-5,0),
            pg.K_RIGHT:(5,0)
        }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool,bool]:
    """
    引数で与えられたRectが画面内か画面外かを判定する関数
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向，縦方向判定結果（True: 画面内，False: 画面外）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦方向判定
        tate = False
    return yoko, tate


def game_over(screen):
    """
    ゲームオーバー画面を表示する
    引数:screen
    """

    black_img=pg.Surface((WIDTH, HEIGHT)) #黒い背景
    pg.draw.rect(black_img, (0,0,0), (0,0,WIDTH, HEIGHT)) #黒い背景を描画

    black_img.set_alpha(200) #黒い背景の透明度を設定

    font=pg.font.Font(None,80) #フォントを設定
    txt=font.render("Game Over", True, (255,255,255)) #ゲームオーバーのテキストを描画
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2

    kk_crying_img = pg.image.load("fig/8.png") #こうかとんの泣いている画像を読み込む
    kk_crying_rct1 = kk_crying_img.get_rect()
    kk_crying_rct1.topleft = WIDTH // 2 - 200, HEIGHT // 2 -50
    kk_crying_rct2 = kk_crying_img.get_rect()
    kk_crying_rct2.topleft = WIDTH // 2 + 200, HEIGHT // 2-50

    black_img.blit(txt, txt_rct)
    black_img.blit(kk_crying_img, kk_crying_rct1)
    black_img.blit(kk_crying_img, kk_crying_rct2)

    screen.blit(black_img, (0,0)) #ゲームオーバー画面を表示
    pg.display.update() #画面を更新
    time.sleep(5)  # 5秒間表示

def init_bb_imgs()->tuple[list[pg.Surface],list{int}]
    for r in range(1, 11):
        bb_img=pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img, (255,0,0), (10*r,10*r), 10*r) #爆弾円
        bb_imgs = []
        bb_accs = [a for a in range(1, 11)] # 加速度リスト 1〜10
        for r in range(1, 11):
        bb_img = pg.Surface((20r, 20r))
        bb_img.set_colorkey((0, 0, 0)) # 黒を透明化
        pg.draw.circle(bb_img, (255, 0, 0), (10r, 10r), 10*r)
        bb_imgs.append(bb_img)
        return bb_imgs, bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20,20))#爆弾用の空
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10) #爆弾円
    bb_img.set_colorkey((0,0,0)) #爆弾の黒を透明に
    bb_rct = bb_img.get_rect() #爆弾Rectを取得
    bb_rct.centerx = random.randint(0, WIDTH) #爆弾のx座標をランダムに
    bb_rct.centery = random.randint(0, HEIGHT) #爆弾のy座標をランダムに
    vx,vy=+5,+5 #爆弾の速度を設定
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾の衝突判定
            print("ゲームオーバー")
            game_over(screen)  # ゲームオーバー画面を表示
            return  # ゲームオーバーの意味でmain関数から出る
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0]+=mv[0]
                sum_mv[1]+=mv[1]
        kk_rct.move_ip(sum_mv)  
        if check_bound(kk_rct) != (True, True):  # 画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)#爆弾を移動

        idx = min(tmr // 500, 9) # 500フレームごとに段階アップ
        bb_img = bb_imgs[idx]
        # サイズが変わったのでRectのサイズを更新（中心は維持）
        curr_center = bb_rec.center
        bb_rec = bb_img.get_rect()
        bb_rec.center = curr_center
    
        # 加速度を適用した速度で移動
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]


        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向の判定
            vx *= -1
        if not tate:  # 縦方向の判定
            vy *= -1

        screen.blit(bb_img, bb_rct)#爆弾を表示
        pg.display.update()
        tmr += 1
        clock.tick(50)

        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
#a