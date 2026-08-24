import pygame

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Fairly easy  :)")
clock = pygame.time.Clock()
OrigPlayer = pygame.image.load('Player.png').convert_alpha()
OrigClown = pygame.image.load('Clown.png').convert_alpha()
OrigBackground = pygame.image.load('PumpkinField.png').convert()
OrigSeed = pygame.image.load('Seed.png').convert_alpha()
OrigTree = pygame.image.load('Tree.png').convert_alpha()
OrigCoin = pygame.image.load('Coin.png').convert_alpha()
OrigInfo = pygame.image.load('PumpkinInfo.png').convert_alpha()
OrigEnoughMoney = pygame.image.load('EnoughMoney.png').convert_alpha()
OrigNEnoughMoney = pygame.image.load('NEnoughMoney.png').convert_alpha()
OrigPumpkinNP = pygame.image.load('PumpkinNP.png').convert_alpha()
OrigPumpkinPass = pygame.image.load('PumpkinPass.png').convert_alpha()

ResizedBackground = pygame.transform.scale(OrigBackground, (1200, 600))
ResizedPlayer = pygame.transform.scale(OrigPlayer, (130, 130))
ResizedClown = pygame.transform.scale(OrigClown, (150, 170))
ResizedSeed = pygame.transform.scale(OrigSeed, (15, 15))
ResizedTree = pygame.transform.scale(OrigTree, (40, 60))
ResizedCoin = pygame.transform.scale(OrigCoin, (120, 110))
ResizedInfo = pygame.transform.scale(OrigInfo, (1100, 550))
ResizedEnoughMoney = pygame.transform.scale(OrigEnoughMoney, (500, 350))
ResizedNEnoughMoney = pygame.transform.scale(OrigNEnoughMoney, (500, 350))
ResizedPumpkinNP = pygame.transform.scale(OrigPumpkinNP, (1050, 550))
ResizedPumpkinPass = pygame.transform.scale(OrigPumpkinPass, (1050, 550))

PumpkinNPRect = ResizedPumpkinNP.get_rect(center=(600, 300))
LightBlueRect = pygame.Rect(975, 250, 50, 100)

PlayerLeft = pygame.transform.flip(ResizedPlayer, True, False)
ClownLeft = pygame.transform.flip(ResizedClown, True, False)

PlayerPosCheck = ResizedPlayer
ClownPosCheck = ResizedClown

PlayerRect = ResizedPlayer.get_rect()
PlayerRect.center = (600, 300)
PlayerHitbox = PlayerRect.inflate(-50, -20)
ClownRect = ResizedClown.get_rect()
ClownRect.center = (15, 15)
ClownHitbox = ClownRect.inflate(-70, -30)

ClownX = float(ClownRect.x)
ClownY = float(ClownRect.y)

PlayerSpeed = 3
ClownSpeed = 0.25
SeedList = []

SeedCooldown = 1000
Growth = 10000
PrevSeed = 0

Coin = 0
ScoreFont = pygame.font.SysFont("Arial", 36, bold=True)

Died = False
Won = False
running = True

ShowInfo = True
InfoRect = ResizedInfo.get_rect(center = (600, 300))
while ShowInfo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ShowInfo = False
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                ShowInfo = False

    screen.blit(ResizedBackground, (0, 0))
    screen.blit(ResizedInfo, InfoRect)
    pygame.display.flip()
    clock.tick(60)

PrevSeed = pygame.time.get_ticks()

while running:
    CurrentTime = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                CurrentTime = pygame.time.get_ticks()

                if CurrentTime - PrevSeed >= SeedCooldown:
                    SeedRect = ResizedSeed.get_rect()
                    SeedRect.center = PlayerRect.center
                    SeedList.append({
                        "Rect": SeedRect,
                        "Spawn": CurrentTime
                    })

                    PrevSeed = CurrentTime
    if not Died and not Won:
        keys = pygame.key.get_pressed()

        if Coin >= 80 and PlayerHitbox.colliderect(LightBlueRect):
            Won = True

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            PlayerRect.x -= PlayerSpeed
            PlayerPosCheck = PlayerLeft
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            PlayerRect.x += PlayerSpeed
            PlayerPosCheck = ResizedPlayer
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            PlayerRect.y -= PlayerSpeed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            PlayerRect.y += PlayerSpeed

        if PlayerRect.left < 25:
            PlayerRect.left = 25
        if PlayerRect.right > 1070:
            PlayerRect.right = 1070
        if PlayerRect.top < 40:
            PlayerRect.top = 40
        if PlayerRect.bottom > 565:
            PlayerRect.bottom = 565

        if ClownRect.centerx < PlayerRect.centerx:
            ClownX += ClownSpeed
            ClownPosCheck = ResizedClown
        elif ClownRect.centerx > PlayerRect.centerx:
            ClownX -= ClownSpeed
            ClownPosCheck = ClownLeft
        if ClownRect.centery < PlayerRect.centery:
            ClownY += ClownSpeed
        elif ClownRect.centery > PlayerRect.centery:
            ClownY -= ClownSpeed

        if Coin >= 20:
            ClownSpeed = 0.4
        if Coin >= 40:
            ClownSpeed = 0.7
        if Coin >= 60:
            ClownSpeed = 1
        if Coin >= 80:
            ClownSpeed = 2

        ClownRect.x = int(ClownX)
        ClownRect.y = int(ClownY)

        PlayerHitbox.center = PlayerRect.center
        ClownHitbox.center = ClownRect.center
        if PlayerHitbox.colliderect(ClownHitbox):
            Died = True
        if Coin >= 80 and PlayerHitbox.colliderect(LightBlueRect):
            Won = True

    screen.blit(ResizedBackground, (0, 0))
    for i in range(len(SeedList) -1, -1, -1):
        Item = SeedList[i]
        if CurrentTime - Item["Spawn"] >= Growth:
            TreeRect = ResizedTree.get_rect()
            TreeRect.center = Item["Rect"].center

            if PlayerRect.colliderect(TreeRect):
                SeedList.pop(i)
                Coin = Coin+1
                continue
            screen.blit(ResizedTree, TreeRect)
        else:
            screen.blit(ResizedSeed, Item["Rect"])
    pygame.draw.rect(screen, (175, 230, 220), (975, 250, 50, 100))
    if Coin >= 80:
        screen.blit(ResizedEnoughMoney, (750, 125))
    else:
        screen.blit(ResizedNEnoughMoney, (750, 125))
    screen.blit(PlayerPosCheck, PlayerRect)
    screen.blit(ClownPosCheck, ClownRect)
    screen.blit(ResizedCoin, (-15, 20))

    #Hitbox Check
    #pygame.draw.rect(screen, (0, 255, 0), PlayerHitbox, 2)
    #pygame.draw.rect(screen, (255, 0, 0), ClownHitbox, 2)
    
    ScoreSurface = ScoreFont.render(str(Coin), True, (255, 255, 255))
    ScoreRect = ScoreSurface.get_rect()
    ScoreRect.topright = (100, 45)
    screen.blit(ScoreSurface, ScoreRect)
    if Died:
        screen.blit(ResizedPumpkinNP, PumpkinNPRect)
        pygame.display.set_caption("Reopen and try again  :)")
    elif Won:
        screen.blit(ResizedPumpkinPass, PumpkinNPRect)
    pygame.display.flip()
    clock.tick(120)
pygame.quit()
