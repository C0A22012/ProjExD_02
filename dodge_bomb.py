import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
delta = {
pg.K_UP: (0, -5),
pg.K_DOWN: (0, +5),
pg.K_LEFT:(-5, 0),
pg.K_RIGHT: (+5, 0),
}


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect、僕弾Rectが画面外 or 画面内かを判定する関数
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向、縦方向の判定結果タプル (True：画面内/False：画面外)
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  #横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  #縦方向判定
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0, 0, 0))
    bd_imgs = [bd_img, pg.transform.rotozoom(bd_img, 10, 1.0)]
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    bd_rct = bd_img.get_rect()
    bd_rct.center = x, y
    bd_imgs =[]
    #1~10の大きさの爆弾の作成
    for r in range(1, 11):
            #一辺が20*rの正方形Suface
            bd_img = pg.Surface((20*r, 20*r))
            #中心に半径10*rの赤い円を描画
            pg.draw.circle(bd_img, (255, 0, 0), (10*r, 10*r), 10*r)
            #爆弾以外の部分にある黒を透過させる
            bd_img.set_colorkey((0, 0, 0))
            bd_imgs.append(bd_img)


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bd_rct):
            print("ゲームオーバー")
            kk_img = pg.image.load("ex02/fig/8.png")
            pg.time.wait(3000)
            return  #　ゲームオーバー
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, mv in delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        bd_rct.move_ip(vx, vy)
        bd_img = bd_imgs[min(tmr//500, 9)]

        yoko, tate = check_bound(bd_rct)
        if not yoko:  #横方向の画面外なら
            vx *= -1
        if not tate:  #縦方向の画面外なら
            vy *= -1
        screen.blit(bd_img, bd_rct)
        pg.display.update()
        tmr += 1
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()