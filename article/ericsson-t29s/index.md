---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20200625125903/https://petermolnar.net/article/ericsson-t29s/
lang: hu
published: '2002-04-27T12:41:26+02:00'
summary: Baromira elegem lett abból, hogy mindig, minden oldalon csak reklámok
    vannak, de valódi cuccok nem, hát gondoltam felteszek néhányat saját tapasztalatok
    alapján.
tags:
- mobile
title: Ericsson T29s
review:
    best: 5
    brand: Ericsson
    model: T29s
    description: GSM telefon
    img: t29s.jpg
    caption: Ez a telefon megvan, és 2020-ban, az eredeti akksival, egy szó nélkül működik ám
    rating: 4
    url: https://www.gsmarena.com/ericsson_t29s-225.php
---

*Ez egy ősi bejegyzés; az oldalam 2002-es mentéséből vakartam elő. Egyre
jobban elszomorít, hogy bárhova nézek, a 20 évvel ezelőtti internetből
minden halott, de sajnos ehhez én is hozzájárultam. Miután ráleltem
erre, és sikerült átformázom az eredeti Windows-1250 szövegkódolásból,
és visszateszem az internetre így majd 20 évvel később, mert miért ne.
Ha jól emlékszem, akkor Windows 2000-rem volt - ha esetleg használni
akarod a letölthető programokat.*

Mivel eddig összesen két telefonom volt, most a komolyabbról lesz egy
kis szó. Technikai adatokat nem írok, azt megtalálhatjátok a Westel vagy
a Sony-Ericsson honlapján. Azonban rögtön fűznék is pár dolgot a
leírásokhoz:

1.  a telefonban nincs beépített modem, bárhol bármit is olvastál
2.  EMS fogadására nem minden telefonról képes (pl. Siemens A50esnél kép
    nem jön át)

## Kódok

IMEI megnézése
:   `*#06#` - az IMEI egy azonosító, ami állítólag minden mobilnál más
    és más. Ha levesszük az akist, általában ott van egy kis cédula,
    rajta ezzel a számmal. Hogy a telefon lopott-e, könnyen ki lehet
    deríteni, csak le kell ellenőrizni, hogy a két szám egyezik-e.
    Ugyanis ha a telefont letiltják, attól még lehet használni, ha
    átírják az IMEI számát. Ez mellesleg MINDEN telefonnál működik.

Telefon kódok aktívak-e:
:   `<**<`

Szervíz menü
:   `>*<<*<`

## Pár szó a telefonok szoftvereiről

**FLASH**: leginkább, mint a telefon operációs rendszerét lehet
elképzelni. Magába foglalja a menüket, a szolgáltatásokat, a támogatott
nyelveket, stb...Így lehet pl. hogy az Ericsson két telefonja, a T10 és
a T18 szinte egy az egyben megegyezik fizikailag, csak a "lelkük", tehát
a rendszerük más.

**EEPROM**: ez a szolgáltató és a felhasználó sajátbeállításait
tartalmazó rész. Ide tartozik pl. a wap beállításoktól kezdve a
csengőhangokon és a bejelentkező animációkon keresztül az IMEI számig
minden.

## Az Ericsson adatkábelekről

Az Ericsson újabb típusú csatlakozóinál (R320, T28, és felfele)
alapvatően kétféle kábel van: az *adat* és a *szervíz*kábel. Randa
üzleti fogás, hogy mindkettőt "data kábel" néven árulják - ami igaz is,
ám az átlag halandó csak igen keservesen jöhet rá, mi a különbség. Pedig
egyszerű: mindössze három forrasztás. (az ötletért köszönet JFox-nak,
<http://www.freeweb.hu/hec>):

> Válaszolnék neked, de az e-mail címedrõm mindíg visszajön a levél. De
> a lényeget itt is le tudom írni. Az a kábel, amivel függetleníted a
> telcsit, az nem jó a MyAnimation-hoz. Én is sokat kínlódtam vele mire
> rájöttem ,hogy milyen kábel kell. A legegyszerûbb, ha veszel egy
> Ericsson DRS-11 kábelt. De ez nem túl pénztárcakímélõ megoldás. A
> másik megoldás, ha veszel a pl. a Corában egy Ericsson T28 adatkábelt
> 2500Ft (ennek árulják, de service kábel!!) és átalakítod. A megoldás a
> kovetkezõ: A telefonra csatlakozó végét a kábelnek óvatosan szét kell
> pattintani. ( \[\]12345678\[\]9\[\]10\|11\[\] ) Ez a telefon alja akar
> lenni.:-) Van itt egy átkötés 11-9 lábakon. Ezt meg kell szüntetni, és
> a 7 ,6 lábakon levõ vezetékeket át forrasztani az 5, 4 lábakra. Ennyi.
> Ja és csak saját felelõsségedre kísérletezz!!! Ha nem vagy otthon az
> elektronikában akkor inkább kérj meg valakit aki ért hozzá! Ha
> valakinek kell van rajz is a kábelrõl.

Az *adatkábel*: ezen keresztül lehet pl. sms-t küldeni, telefonkönyvet
szerkeszteni a gépen, vagy épp modemnek használni a telefont. Az ára
6200 Ft- 11000 Ft. Az eredeti, az Ericsson RDS-11 kerül 11000 Ft-ba.

A *szervízkábel*: ezzel lehet mindenféle randaságot csinálni, pl.
kioldani a SIM-zárat, lecserélni az IMEI-t, átírni a szoftvert...szóval
mindent, ami illegális. Az ára 2500 - 5000 Ft...

## Letöltések

SZERVÍZKÁBEL kell:

-   [Ericsson T29s FLASH file - 2 MB](t29_flash.rar), a saját
    telefonomról, európai nyelvtámogatással
-   [Ericsson T29s EEPROM - 4.6 KB](t29_eeprom.rar), VIGYÁZZ!!!! egy
    francia szolgáltató logoját teszi ki animációnak a Westel, Pannon,
    Voda vagy Ericsson helyett és minden sajátbeállítást töröl!!!
    (csengőhangok, telefonbeli sms-ek, telefonbeli telefonszámok, wap és
    gprs beállítás, stb, a SIM-hez nem nyúl)
-   [Ericsson A2628, T20 és T29 szervíz szoftver - 325
    KB](ericsson_t29_service_software.exe), hogy az előző kettőt
    használni tudd

ADATKÁBEL kell:

-   [Easytext 1.7c - 816 KB](easytext.exe), egyszerű mobilkezelő gépen,
    kicsit csúf, de ingyenes és használható
-   [MyAnimation - 692 KB](myanimation.exe), bejelentkezőanimációt lehet
    vele csinálni; animáció képalbumok:
-   [Portfolio 1 - 5.04 KB](portfolio.exe)
-   [Portfolio 2 - 35.2 KB](portfolio2.rar)
-   [Csengőhangok - 26.7 KB](ericsson_ringtones.exe), bepötyögni vagy az
    Easytext-el átküldeni, txt formátum

## Ericsson Mobile Office Suite

Ez egy Ericsson által kiadott program, amivel szinkronizálni lehet a
címjegyzék és az sms-ek között a teleofn és pl. a Személyes Címjegyzék
vagy az Outlook között. Kicsit bonyolult használni, de rá lehet jönni.
Amit tudni kell róla:

-   csak Windows 9x alatt sikerült működtetnem.
-   A telepítéskor modemet kell felinstallálni, hogy lássa a telefont. A
    modemek listából ki kell választani egy "Standard modem 9600 bps"
    feliratút, így működni fog. Ennek ellenére a telefont nem lehet
    modemnak használni, sajnos.
-   Érdekes tulajdonsága, hogy a "ő" betűt nem ismer, illetve "ó" betű
    esetén a telefonban az "ó" és az azt megelőző betű el fog tűnni....

## Csengőhangok

The Godfather v1
:   `EA+CBA+CABAFGEpppppEA+CBA+CABAE#DD`

The Godfather v2
:   `CF#GGF#GFGF#C#DC`

Kraftwerk - The Model v1
:   `eAAa+cbaBpgEppAppp+cbaBpgE`

Kraftwerk - The Model v2
:   `+e+ca+c+e+c+e+f+e+ca+c+E+D+e+ca+c+e+c+e+f+e+ca+c+E+D`

Mike Oldfield - Tubular Bells v1
:   `eaebegae+ce+deb+cebeaebegae+ce+deb+c`

Mike Oldfield - Tubular Bells v2
:   `eaebegae+ce+deb+ceaebagae+ce+deb+cebeaebegae+ce+deb+ceaebegae+ce+deb+cebeaebega`

Star Trek
:   `CppfaG#dp#d+d+Cppppa#a+c+d#a+Cp#ApApafaG`
