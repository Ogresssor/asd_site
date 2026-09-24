# Пакет фото для загрузки в каталог по утверждённому дереву.
# Источник: images/ (извлечено из архива заказчика). Результат: foto/
import os, glob, shutil, csv
from PIL import Image

SRC = {os.path.splitext(os.path.basename(p))[0]: p for p in glob.glob('images/**/*.*', recursive=True)}
OUT = 'foto'
SIZE = 1000

# (раздел, картинка раздела, [(подраздел, картинка подраздела, [(позиция, код, [фото...])])])
TREE = [
 ('Тепловые пункты и автоматизация', 'blochnyy-teplovoy-punkt-btp', [
   ('Шкафы автоматизации и учёта', 'shkaf-avtomatizacii', [
     ('Шкаф учёта', 'shkaf-ucheta', ['shkaf-ucheta']),
     ('Шкаф автоматизации', 'shkaf-avtomatizacii', ['shkaf-avtomatizacii'])]),
   ('Блочные тепловые пункты', 'blochnyy-teplovoy-punkt-btp', [
     ('Блочный тепловой пункт (БТП)', 'blochnyy-teplovoy-punkt-btp', ['blochnyy-teplovoy-punkt-btp'])])]),
 ('Насосное оборудование', 'cirkulyacionnyy-nasos-wilo-cronoline-il-flancevyy', [
   ('Циркуляционные насосы', 'cirkulyacionnyy-nasos-native-noc-s-rezbovoy-flancevyy', [
     ('Циркуляционный насос (резьбовой/фланцевый)', 'cirkulyacionnyy-nasos',
      ['cirkulyacionnyy-nasos-native-noc-s-rezbovoy-flancevyy', 'cirkulyacionnyy-nasos-wilo-cronoline-il-flancevyy'])]),
   ('Насосные установки', 'nasosnaya-ustanovka-povysheniya-davleniya', [
     ('Насосная установка повышения давления', 'nasosnaya-ustanovka-povysheniya-davleniya', ['nasosnaya-ustanovka-povysheniya-davleniya']),
     ('Насосная установка пожаротушения', 'nasosnaya-ustanovka-pozharotusheniya', ['nasosnaya-ustanovka-pozharotusheniya']),
     ('Насосная установка поддержания давления', 'nasosnaya-ustanovka-podderzhaniya-davleniya', ['nasosnaya-ustanovka-podderzhaniya-davleniya'])]),
   ('Центробежные насосы', 'centrobezhnyy-nasos', [('Центробежный насос', 'centrobezhnyy-nasos', ['centrobezhnyy-nasos'])]),
   ('Канализационные насосы', 'kanalizacionnyy-nasos', [('Канализационный насос', 'kanalizacionnyy-nasos', ['kanalizacionnyy-nasos'])]),
   ('Насосы инлайн', 'nasos-inlayn', [('Насос инлайн', 'nasos-inlayn', ['nasos-inlayn'])]),
   ('Консольные насосы', 'konsolno-monoblochnyy-nasos', [('Консольно-моноблочный насос', 'konsolno-monoblochnyy-nasos', ['konsolno-monoblochnyy-nasos'])]),
   ('Многоступенчатые насосы', 'mnogostupenchatyy-nasos-vertikalnyy', [
     ('Многоступенчатый насос (горизонтальный/вертикальный)', 'mnogostupenchatyy-nasos',
      ['mnogostupenchatyy-nasos-vertikalnyy', 'mnogostupenchatyy-nasos-gorizontalnyy'])]),
   ('Дренажные насосы', 'drenazhnyy-nasos', [('Дренажный насос', 'drenazhnyy-nasos', ['drenazhnyy-nasos'])]),
   ('Фекальные насосы', 'fekalnyy-nasos', [('Фекальный насос', 'fekalnyy-nasos', ['fekalnyy-nasos'])]),
   ('Поверхностные насосы', 'poverhnostnyy-nasos', [('Поверхностный насос', 'poverhnostnyy-nasos', ['poverhnostnyy-nasos'])])]),
 ('Теплообменное оборудование', 'plastinchatyy-teploobmennik', [
   ('Пластинчатые теплообменники', 'plastinchatyy-teploobmennik', [
     ('Теплообменник (паяный/разборный)', 'teploobmennik', ['plastinchatyy-teploobmennik'])]),
   ('Комплектующие теплообменников', 'prokladka-dlya-teploobmennika', [
     ('ЗИП для теплообменника (пластины, прокладки)', 'zip-dlya-teploobmennika', ['prokladka-dlya-teploobmennika']),
     ('Теплоизоляция для теплообменника', 'teploizolyaciya-dlya-teploobmennika', ['termochehol'])])]),
 ('Трубопроводная арматура', 'kran-sharovoy-stalnoy', [
   ('Стальная арматура', 'kran-sharovoy-stalnoy', [
     ('Кран шаровой стальной (резьба, фланец, приварка)', 'kran-sharovoy-stalnoy', ['kran-sharovoy-stalnoy']),
     ('Запорно-регулирующий клапан', 'zaporno-reguliruyuschiy-klapan', []),
     ('Антивибрационный компенсатор (муфтовый/фланцевый)', 'antivibracionnyy-kompensator', ['antivibracionnyy-kompensator'])]),
   ('Чугунная арматура', 'zatvor-chugunnyy', [
     ('Обратный клапан', 'obratnyy-klapan-chugunnyy', ['obratnyy-klapan-chugunnyy']),
     ('Фильтр', 'filtr-chugunnyy', ['filtr-chugunnyy']),
     ('Затвор (ручка/редуктор/привод)', 'zatvor-chugunnyy', ['zatvor-chugunnyy']),
     ('Задвижка с обрезиненным клином', 'zadvizhka-s-obrezinennym-klinom', []),
     ('Шиберная ножевая задвижка', 'shibernaya-nozhevaya-zadvizhka', [])]),
   ('Латунная арматура', 'kran-sharovoy-latunnyy', [
     ('Кран шаровой', 'kran-sharovoy-latunnyy', ['kran-sharovoy-latunnyy']),
     ('Обратный клапан', 'obratnyy-klapan-latunnyy', ['obratnyy-klapan-latunnyy']),
     ('Фильтр', 'filtr-latunnyy', ['filtr-latunnyy'])]),
   ('Балансировочные клапаны', 'kombinirovannyy-balansirovochnyy-klapan-aqf-r-flancevyy', [
     ('Ручной балансировочный клапан MNT-R, MVT-R2 (резьбовой)', 'ruchnoy-balansirovochnyy-klapan-rezbovoy',
      ['ruchnoy-balansirovochnyy-klapan-mnt-r-rezbovoy', 'ruchnoy-balansirovochnyy-klapan-mvt-r2-rezbovoy']),
     ('Ручной балансировочный клапан MNF-R2 (фланцевый)', 'ruchnoy-balansirovochnyy-klapan-flancevyy', ['ruchnoy-balansirovochnyy-klapan-mnf-r2-flancevyy']),
     ('Автоматический балансировочный клапан AQT-R3, AQF-R', 'avtomaticheskiy-balansirovochnyy-klapan',
      ['kombinirovannyy-balansirovochnyy-klapan-aqt-r3-rezbovoy', 'kombinirovannyy-balansirovochnyy-klapan-aqf-r-flancevyy']),
     ('Регулятор перепада давления APT-R3', 'regulyator-perepada-davleniya-apt-r3', ['regulyator-perepada-davleniya-apt-r3'])]),
   ('Предохранительные клапаны', 'predohranitelnyy-klapan', [
     ('Предохранительный клапан', 'predohranitelnyy-klapan', ['predohranitelnyy-klapan'])]),
   ('Арматура для систем пожаротушения', None, [
     ('Затворы', 'zatvory-pozharotushenie', []),
     ('Задвижки', 'zadvizhki-pozharotushenie', []),
     ('Обратные клапаны', 'obratnye-klapany-pozharotushenie', [])])]),
 ('Трубы и фитинги', 'truba-iz-sshitogo-polietilena', [
   ('Трубы из сшитого полиэтилена и металлопластика', 'truba-iz-sshitogo-polietilena', [
     ('Труба PEX-a', 'truba-pex-a', ['truba-iz-sshitogo-polietilena']),
     ('Труба металлопластиковая', 'truba-metalloplastikovaya', ['truba-metalloplastikovaya'])]),
   ('Полипропиленовые трубы и фитинги', 'fiting-polipropilenovyy', [
     ('Полипропиленовая труба', 'polipropilenovaya-truba', ['polipropilenovaya-truba']),
     ('Фитинг полипропиленовый', 'fiting-polipropilenovyy', ['fiting-polipropilenovyy'])])]),
 ('Отопление', 'stalnoy-panelnyy-radiator', [
   ('Радиаторы', 'stalnoy-panelnyy-radiator', [
     ('Стальной панельный радиатор', 'stalnoy-panelnyy-radiator', ['stalnoy-panelnyy-radiator']),
     ('Биметаллический радиатор', 'bimetallicheskiy-radiator', ['bimetallicheskiy-radiator'])]),
   ('Конвекторы', 'vnutripolnyy-konvektor', [
     ('Напольный конвектор', 'napolnyy-konvektor', ['napolnyy-konvektor']),
     ('Внутрипольный конвектор', 'vnutripolnyy-konvektor', ['vnutripolnyy-konvektor'])]),
   ('Расширительные баки', 'membrannyy-rasshiritelnyy-bak', [
     ('Мембранный расширительный бак', 'membrannyy-rasshiritelnyy-bak', ['membrannyy-rasshiritelnyy-bak'])]),
   ('Коллекторы', 'kollektornyy-shkaf', [
     ('Коллекторный шкаф', 'kollektornyy-shkaf', ['kollektornyy-shkaf']),
     ('Узлы распределительные этажные', 'uzly-raspredelitelnye-etazhnye', []),
     ('Коллекторы распределительные', 'kollektory-raspredelitelnye', [])])]),
 ('Приборы учёта и КИПиА', 'teploschetchik', [
   ('Счётчики воды', 'schetchik-vody-krylchatyy', [
     ('Счётчик воды (бытовые/промышленные/турбинные)', 'schetchik-vody', ['schetchik-vody-krylchatyy', 'schetchik-vody-ultrazvukovoy'])]),
   ('Теплоучёт и энергосбережение', 'teploschetchik', [
     ('Теплосчётчик', 'teploschetchik', ['teploschetchik']),
     ('Расходомер', 'rashodomer', ['rashodomer']),
     ('Датчики', 'datchiki', ['datchik'])]),
   ('КИПиА', 'manometr', [
     ('Манометр', 'manometr', ['manometr']),
     ('Термометр', 'termometr', ['termometr']),
     ('Термоманометр', 'termomanometr', ['termomanometr'])])]),
 ('Вентиляция и климат', 'teplovaya-zavesa', [
   ('Климатическое оборудование', 'teplovaya-zavesa', [
     ('Тепловентилятор', 'teploventilyator', ['teploventilyator']),
     ('Тепловая завеса', 'teplovaya-zavesa', ['teplovaya-zavesa']),
     ('Сплит-система', 'split-sistema', ['split-sistema']),
     ('Чиллер', 'chiller', ['chiller'])]),
   ('Противопожарные клапаны', 'protivopozharnyy-klapan', [
     ('Противопожарный клапан', 'protivopozharnyy-klapan', ['protivopozharnyy-klapan'])])]),
 ('Изоляция', 'kauchukovaya-teploizolyaciya', [
   ('Теплоизоляция', 'kauchukovaya-teploizolyaciya', [
     ('Изоляция из вспененного каучука', 'izolyaciya-iz-vspenennogo-kauchuka', ['kauchukovaya-teploizolyaciya']),
     ('Изоляция из вспененного полиэтилена', 'izolyaciya-iz-vspenennogo-polietilena', ['podlozhka-iz-vspenennogo-polietilena']),
     ('Высокотемпературная изоляция', 'vysokotemperaturnaya-izolyaciya', []),
     ('Изоляция для воздуховодов', 'izolyaciya-dlya-vozduhovodov', []),
     ('Промышленная теплоизоляция', 'promyshlennaya-teploizolyaciya', []),
     ('Цилиндры из минеральной ваты', 'cilindry-iz-mineralnoy-vaty', ['cilindr-iz-mineralnoy-vaty', 'cilindr-iz-mineralnoy-vaty-shumoizolyaciya']),
     ('Аксессуары (клей, лента, очиститель)', 'aksessuary-dlya-izolyacii', ['kley', 'lenta'])]),
   ('Звукоизоляция', 'k-fonik', [
     ('K-Fonik (ST / fiber / GK / open cell / zip case)', 'k-fonik', ['k-fonik']),
     ('SOUNDLOCK K-FONIK GK', 'soundlock-k-fonik-gk', [])])]),
]
UNUSED = ['kanalizacionnaya-truba', 'trap', 'voronka']

def save(src_key, dst):
    im = Image.open(SRC[src_key])
    if im.mode in ('P', 'LA', 'RGBA') or 'transparency' in im.info:
        im = im.convert('RGBA')
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg
    im = im.convert('RGB')
    im.thumbnail((int(SIZE * 0.9), int(SIZE * 0.9)), Image.LANCZOS)
    canvas = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))
    canvas.paste(im, ((SIZE - im.width) // 2, (SIZE - im.height) // 2))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    canvas.save(dst, 'JPEG', quality=85, optimize=True, progressive=True)

shutil.rmtree(OUT, ignore_errors=True)
rows, missing = [], []
for i, (sec, sec_img, subs) in enumerate(TREE, 1):
    sdir = f'{OUT}/{i:02d} {sec}'
    save(sec_img, f'{sdir}/_картинка раздела.jpg')
    for j, (sub, sub_img, items) in enumerate(subs, 1):
        ddir = f'{sdir}/{i:02d}.{j:02d} {sub}'
        os.makedirs(ddir, exist_ok=True)
        if sub_img: save(sub_img, f'{ddir}/_картинка подраздела.jpg')
        else: missing.append(f'{sec} / {sub} — картинка подраздела')
        for name, code, photos in items:
            if not photos:
                missing.append(f'{sec} / {sub} / {name}  ({code})')
            for k, p in enumerate(photos):
                fn = f'{code}.jpg' if k == 0 else f'{code}_доп{k}.jpg'
                save(p, f'{ddir}/{fn}')
            rows.append([sec, sub, name, code, len(photos)])
for k in UNUSED:
    save(k, f'{OUT}/_не вошло в структуру (канализация)/{k}.jpg')
with open(f'{OUT}/_НЕТ ФОТО.txt', 'w', encoding='utf-8-sig') as f:
    f.write('Позиции без фото — запросить у заказчика:\n\n' + '\n'.join(missing) + '\n')
print('позиций:', len(rows), '| с фото:', sum(1 for r in rows if r[4]), '| без фото:', len(missing))
