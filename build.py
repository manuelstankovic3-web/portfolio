"""Builds the Fresh Front site in every language.

Edit the texts in T below (or the layout in src/template.html), then run:
    python3 build.py
It writes index.html (Croatian) and en/, de/, ru/, es/ index.html files.
"""
import os
import re
from urllib.parse import quote

SITE = "https://freshfront.eu"
CAL = "https://cal.com/manuel-stankovic/15min"
ROOT = os.path.dirname(os.path.abspath(__file__))

LATIN_FONTS = (
    "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800"
    "&family=Atkinson+Hyperlegible:wght@400;700&display=swap",
    '"Bricolage Grotesque", system-ui, sans-serif',
    '"Atkinson Hyperlegible", system-ui, sans-serif',
)
# Bricolage and Atkinson have no Cyrillic, so Russian uses Onest for everything.
CYRILLIC_FONTS = (
    "https://fonts.googleapis.com/css2?family=Onest:wght@400;500;700;800&display=swap",
    '"Onest", system-ui, sans-serif',
    '"Onest", system-ui, sans-serif',
)

# Order of the flags in the language bar.
LANGS = ["hr", "en", "de", "ru", "es"]
PATHS = {"hr": "/", "en": "/en/", "de": "/de/", "ru": "/ru/", "es": "/es/"}
NAMES = {"hr": "Hrvatski", "en": "English", "de": "Deutsch", "ru": "Русский", "es": "Español"}

FLAGS = {
    "hr": (
        '<svg viewBox="0 0 30 20" aria-hidden="true">'
        '<rect width="30" height="20" fill="#171796"/><rect width="30" height="13.33" fill="#fff"/>'
        '<rect width="30" height="6.67" fill="#FF0000"/>'
        '<path d="M11.5 5.2h7v6.3c0 2.3-1.6 3.6-3.5 4.3-1.9-.7-3.5-2-3.5-4.3z" fill="#fff" stroke="#171796" stroke-width=".4"/>'
        '<path d="M11.5 5.2h1.4v1.4h-1.4zM14.3 5.2h1.4v1.4h-1.4zM17.1 5.2h1.4v1.4h-1.4z'
        'M12.9 6.6h1.4V8h-1.4zM15.7 6.6h1.4V8h-1.4z'
        'M11.5 8h1.4v1.4h-1.4zM14.3 8h1.4v1.4h-1.4zM17.1 8h1.4v1.4h-1.4z'
        'M12.9 9.4h1.4v1.4h-1.4zM15.7 9.4h1.4v1.4h-1.4z'
        'M11.6 10.8h1.3v1.3h-1.1zM14.3 10.8h1.4v1.4h-1.4zM17.1 10.8h1.3l-.1 1.3h-1.2z'
        'M12.9 12.2h1.4v1.4h-1.4zM15.7 12.2h1.4v1.4h-1.4zM14.3 13.6h1.4v1.5l-.7.4-.7-.4z" fill="#FF0000"/>'
        "</svg>"
    ),
    "en": (
        '<svg viewBox="0 0 60 30" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
        '<clipPath id="ukc"><path d="M30,15h30v15zv15h-30zh-30v-15zv-15h30z"/></clipPath>'
        '<path d="M0,0v30h60v-30z" fill="#012169"/>'
        '<path d="M0,0L60,30M60,0L0,30" stroke="#fff" stroke-width="6"/>'
        '<path d="M0,0L60,30M60,0L0,30" clip-path="url(#ukc)" stroke="#C8102E" stroke-width="4"/>'
        '<path d="M30,0v30M0,15h60" stroke="#fff" stroke-width="10"/>'
        '<path d="M30,0v30M0,15h60" stroke="#C8102E" stroke-width="6"/>'
        "</svg>"
    ),
    "de": (
        '<svg viewBox="0 0 30 20" aria-hidden="true">'
        '<rect width="30" height="20" fill="#FFCE00"/><rect width="30" height="13.33" fill="#DD0000"/>'
        '<rect width="30" height="6.67" fill="#000"/></svg>'
    ),
    "ru": (
        '<svg viewBox="0 0 30 20" aria-hidden="true">'
        '<rect width="30" height="20" fill="#D52B1E"/><rect width="30" height="13.33" fill="#0039A6"/>'
        '<rect width="30" height="6.67" fill="#fff"/></svg>'
    ),
    "es": (
        '<svg viewBox="0 0 30 20" aria-hidden="true">'
        '<rect width="30" height="20" fill="#AA151B"/><rect y="5" width="30" height="10" fill="#F1BF00"/></svg>'
    ),
}

T = {
    "hr": {
        "title": "Fresh Front – web stranice za firme diljem Hrvatske",
        "description": "Moderne web stranice za male firme diljem Hrvatske: prilagođene mobitelima, vidljive na Googleu, s online rezervacijama. Besplatan koncept bez obveze.",
        "og_description": "Nova web stranica za vašu firmu za oko tjedan dana. Besplatan koncept bez obveze.",
        "lang_nav_label": "Odaberite jezik",
        "brand_sub": "web stranice",
        "nav_inquiry": "Pošaljite upit",
        "subj_inquiry": "Upit za web stranicu",
        "subj_concept": "Besplatan koncept stranice",
        "h1": "Nova web stranica za vašu firmu, gotova za tjedan dana.",
        "lead": "Izrađujem stranice za konobe, servise, ordinacije, salone i obrte diljem Hrvatske. Prije bilo kakvog dogovora dobijete besplatan koncept, pa vidite što dobivate.",
        "cta_concept": "Zatražite besplatan koncept",
        "cta_prices": "Pogledajte cijene",
        "cta_call": "Rezervirajte razgovor od 15 min",
        "compare_label": "Usporedba stare i nove web stranice na mobitelu",
        "old_bar": "KONOBA MUL - DOBRODOŠLI NA NAŠU WEB STRANICU",
        "old_nav": "Home | O nama | Specijaliteti | Galerija | Kontakt | Linkovi",
        "old_body": "Dobrodošli u konobu Mul. Nalazimo se uz more, u mirnoj uvali. Nudimo domaću hranu, ribu, meso s roštilja i domaće slastice. Pogledajte naše specijalitete u izborniku iznad.",
        "old_price": "Cijene: riblja plata 165,76 kn / 22,00 €",
        "old_notice": "Rezervacije isključivo telefonom!",
        "old_foot": "© 2017 Konoba Mul | Sva prava pridržana",
        "tag_before": "Prije",
        "tag_after": "Poslije",
        "new_sub": "Riba, roštilj i domaće slastice uz more",
        "new_meta": "Otvoreno danas 12–23 h<br>Jelovnik s cijenama u eurima",
        "new_cta": "Rezervirajte stol",
        "new_cta2": "Nazovite nas",
        "demo_note": "Primjer za izmišljenu konobu, onako kako izgleda na mobitelu.",
        "gets_h2": "Što dobiva vaša firma",
        "gets_intro": "Većina gostiju i klijenata vas danas traži na mobitelu. Stranica mora brzo reći tko ste, što nudite i kako vas dobiti.",
        "g1t": "Izgleda dobro na mobitelu",
        "g1d": "Tekst se čita bez zumiranja, a gumbi za poziv i rezervaciju su odmah pri ruci.",
        "g2t": "Pronađu vas na Googleu",
        "g2d": "Stranica je ispravno postavljena za pretraživanje, s vašim adresom, radnim vremenom i djelatnošću.",
        "g3t": "Rezervacije i upiti online",
        "g3d": "Gost rezervira stol, a klijent se naruči na servis ili pregled i onda kad vi ne stignete javiti se na telefon.",
        "g4t": "Ažurne cijene i informacije",
        "g4d": "Jelovnik, cjenik i radno vrijeme u eurima i na jezicima koje trebate, uvijek točni.",
        "g5t": "Izmjene bez muke",
        "g5d": "Pošaljete mi poruku što treba promijeniti i to je gotovo, bez učenja ikakvih programa.",
        "g6t": "Hosting i domena riješeni",
        "g6d": "Stranica je brza i sigurna (https), a ja se brinem da sve radi.",
        "steps_h2": "Kako to ide",
        "steps_intro": "Ništa ne plaćate dok ne vidite kako bi vaša nova stranica izgledala.",
        "s1t": "Besplatan koncept",
        "s1d": "Javite se i za dan-dva dobijete prijedlog naslovnice za vašu firmu, bez obveze.",
        "s2t": "Dogovor",
        "s2d": f'Ako vam se sviđa, dogovorimo detalje u <a href="{CAL}">kratkom razgovoru od 15 minuta</a>. Plaćate polovicu unaprijed i pošaljete logo, slike i tekstove.',
        "s3t": "Izrada",
        "s3d": "Stranica je gotova za oko tjedan dana. Pregledate je i tražite izmjene dok niste zadovoljni.",
        "s4t": "Objava",
        "s4d": "Plaćate ostatak, a stranica ide online na vašoj domeni. Za izmjene ste mi uvijek dostupni.",
        "prices_h2": "Cijene",
        "prices_intro": "Jasno i unaprijed. Točnu cijenu dogovaramo nakon koncepta, ovisno o tome koliko stranica i funkcija trebate.",
        "p1h": "Nova web stranica",
        "p1amount": "od 350 €",
        "p1unit": "jednokratno",
        "p1note": "Polovica unaprijed, ostatak kad je stranica gotova.",
        "p1a": "Dizajn po mjeri vaše firme",
        "p1b": "Prilagođeno mobitelima i Googleu",
        "p1c": "Obrazac za rezervacije ili upite",
        "p1d": "Postavljanje na vašu domenu",
        "p2h": "Hosting i održavanje",
        "p2unit": "mjesečno",
        "p2note": "Nije obavezno, ali tako ne morate brinuti ni o čemu.",
        "p2a": "Brz i siguran hosting",
        "p2b": "Izmjene cijena, slika i teksta",
        "p2c": "Provjera da sve radi",
        "contact_h2": "Pogledajmo vašu stranicu",
        "contact_p": "Pošaljite mi adresu svoje stranice ili samo ime firme. Javim vam se s besplatnim konceptom nove naslovnice, a vi odlučite želite li nastaviti. Manuel Stanković, Fresh Front",
    },
    "en": {
        "title": "Fresh Front – websites for businesses across Croatia",
        "description": "Modern websites for small businesses across Croatia: mobile-friendly, easy to find on Google, with online bookings. Free concept, no obligation.",
        "og_description": "A new website for your business in about a week. Free concept, no obligation.",
        "lang_nav_label": "Choose a language",
        "brand_sub": "websites",
        "nav_inquiry": "Send an inquiry",
        "subj_inquiry": "Website inquiry",
        "subj_concept": "Free website concept",
        "h1": "A new website for your business, ready in a week.",
        "lead": "I build websites for restaurants, workshops, clinics, salons and small businesses across Croatia. Before anything is agreed, you get a free concept, so you see exactly what you're getting.",
        "cta_concept": "Ask for a free concept",
        "cta_prices": "See prices",
        "cta_call": "Book a 15-minute call",
        "compare_label": "An old and a new website compared on a phone",
        "old_bar": "KONOBA MUL - WELCOME TO OUR WEBSITE",
        "old_nav": "Home | About us | Specialities | Gallery | Contact | Links",
        "old_body": "Welcome to Konoba Mul. We are by the sea, in a quiet bay. We serve home cooking, fish, grilled meat and homemade desserts. See our specialities in the menu above.",
        "old_price": "Prices: fish platter 165,76 kn / 22,00 €",
        "old_notice": "Reservations by phone only!",
        "old_foot": "© 2017 Konoba Mul | All rights reserved",
        "tag_before": "Before",
        "tag_after": "After",
        "new_sub": "Fish, grill and homemade desserts by the sea",
        "new_meta": "Open today 12–11 pm<br>Menu with prices in euros",
        "new_cta": "Book a table",
        "new_cta2": "Call us",
        "demo_note": "An example for an invented restaurant, as it looks on a phone.",
        "gets_h2": "What your business gets",
        "gets_intro": "Most guests and customers look you up on their phone. Your website has to say quickly who you are, what you offer and how to reach you.",
        "g1t": "Looks good on a phone",
        "g1d": "Text is readable without zooming, and the call and booking buttons are right at hand.",
        "g2t": "Easy to find on Google",
        "g2d": "The site is set up properly for search, with your address, opening hours and what you do.",
        "g3t": "Online bookings and inquiries",
        "g3d": "Guests book a table and customers book a service or appointment, even when you can't pick up the phone.",
        "g4t": "Up-to-date prices and information",
        "g4d": "Menu, price list and opening hours in euros and in the languages you need, always correct.",
        "g5t": "Changes without hassle",
        "g5d": "Send me a message with what needs changing and it's done. No software to learn.",
        "g6t": "Hosting and domain taken care of",
        "g6d": "The site is fast and secure (https), and I make sure everything keeps working.",
        "steps_h2": "How it works",
        "steps_intro": "You pay nothing until you've seen what your new website would look like.",
        "s1t": "Free concept",
        "s1d": "Get in touch and within a day or two you receive a homepage proposal for your business, with no obligation.",
        "s2t": "Agreement",
        "s2d": f'If you like it, we settle the details in a <a href="{CAL}">short 15-minute call</a>. You pay half up front and send your logo, photos and texts.',
        "s3t": "Build",
        "s3d": "The site is ready in about a week. You review it and ask for changes until you're happy.",
        "s4t": "Launch",
        "s4d": "You pay the rest and the site goes live on your domain. I'm always available for changes.",
        "prices_h2": "Prices",
        "prices_intro": "Clear and up front. We agree the exact price after the concept, depending on how many pages and features you need.",
        "p1h": "New website",
        "p1amount": "from 350 €",
        "p1unit": "one-off",
        "p1note": "Half up front, the rest when the site is finished.",
        "p1a": "Design made for your business",
        "p1b": "Built for phones and Google",
        "p1c": "Booking or inquiry form",
        "p1d": "Set up on your own domain",
        "p2h": "Hosting and maintenance",
        "p2unit": "per month",
        "p2note": "Optional, but it means you never have to worry about it.",
        "p2a": "Fast, secure hosting",
        "p2b": "Updates to prices, photos and text",
        "p2c": "Regular checks that everything works",
        "contact_h2": "Let's look at your website",
        "contact_p": "Send me your website address or just your business name. I'll get back to you with a free concept for a new homepage, and you decide whether to go ahead. Manuel Stanković, Fresh Front",
    },
    "de": {
        "title": "Fresh Front – Websites für Unternehmen in ganz Kroatien",
        "description": "Moderne Websites für kleine Unternehmen in ganz Kroatien: für Smartphones optimiert, bei Google gut auffindbar, mit Online-Reservierung. Kostenloser Entwurf, unverbindlich.",
        "og_description": "Eine neue Website für Ihr Unternehmen in etwa einer Woche. Kostenloser Entwurf, unverbindlich.",
        "lang_nav_label": "Sprache wählen",
        "brand_sub": "Websites",
        "nav_inquiry": "Anfrage senden",
        "subj_inquiry": "Anfrage Website",
        "subj_concept": "Kostenloser Website-Entwurf",
        "h1": "Eine neue Website für Ihr Unternehmen, fertig in einer Woche.",
        "lead": "Ich erstelle Websites für Restaurants, Werkstätten, Praxen, Salons und Kleinbetriebe in ganz Kroatien. Bevor etwas vereinbart wird, bekommen Sie einen kostenlosen Entwurf und sehen genau, was Sie bekommen.",
        "cta_concept": "Kostenlosen Entwurf anfragen",
        "cta_prices": "Preise ansehen",
        "cta_call": "15-Minuten-Gespräch buchen",
        "compare_label": "Alte und neue Website im Vergleich auf dem Smartphone",
        "old_bar": "KONOBA MUL - WILLKOMMEN AUF UNSERER WEBSITE",
        "old_nav": "Home | Über uns | Spezialitäten | Galerie | Kontakt | Links",
        "old_body": "Willkommen in der Konoba Mul. Wir liegen direkt am Meer, in einer ruhigen Bucht. Wir bieten Hausmannskost, Fisch, Gegrilltes und hausgemachte Desserts. Unsere Spezialitäten finden Sie im Menü oben.",
        "old_price": "Preise: Fischplatte 165,76 kn / 22,00 €",
        "old_notice": "Reservierungen nur telefonisch!",
        "old_foot": "© 2017 Konoba Mul | Alle Rechte vorbehalten",
        "tag_before": "Vorher",
        "tag_after": "Nachher",
        "new_sub": "Fisch, Grill und hausgemachte Desserts am Meer",
        "new_meta": "Heute geöffnet 12–23 Uhr<br>Speisekarte mit Preisen in Euro",
        "new_cta": "Tisch reservieren",
        "new_cta2": "Anrufen",
        "demo_note": "Beispiel für ein erfundenes Restaurant, so wie es auf dem Smartphone aussieht.",
        "gets_h2": "Was Ihr Unternehmen bekommt",
        "gets_intro": "Die meisten Gäste und Kunden suchen Sie heute auf dem Smartphone. Ihre Website muss schnell zeigen, wer Sie sind, was Sie anbieten und wie man Sie erreicht.",
        "g1t": "Sieht auf dem Smartphone gut aus",
        "g1d": "Der Text ist ohne Zoomen lesbar, und die Tasten zum Anrufen und Reservieren sind sofort zur Hand.",
        "g2t": "Bei Google gefunden werden",
        "g2d": "Die Website ist richtig für Suchmaschinen eingerichtet, mit Adresse, Öffnungszeiten und Tätigkeit.",
        "g3t": "Online-Reservierungen und Anfragen",
        "g3d": "Gäste reservieren einen Tisch, Kunden buchen einen Service oder Termin, auch wenn Sie gerade nicht ans Telefon gehen können.",
        "g4t": "Aktuelle Preise und Informationen",
        "g4d": "Speisekarte, Preisliste und Öffnungszeiten in Euro und in den Sprachen, die Sie brauchen, immer korrekt.",
        "g5t": "Änderungen ohne Aufwand",
        "g5d": "Schicken Sie mir eine Nachricht, was geändert werden soll, und es ist erledigt. Kein Programm zu lernen.",
        "g6t": "Hosting und Domain erledigt",
        "g6d": "Die Website ist schnell und sicher (https), und ich sorge dafür, dass alles funktioniert.",
        "steps_h2": "So läuft es ab",
        "steps_intro": "Sie zahlen nichts, bevor Sie gesehen haben, wie Ihre neue Website aussehen würde.",
        "s1t": "Kostenloser Entwurf",
        "s1d": "Melden Sie sich, und in ein bis zwei Tagen erhalten Sie einen Vorschlag für Ihre Startseite, unverbindlich.",
        "s2t": "Vereinbarung",
        "s2d": f'Wenn er Ihnen gefällt, klären wir die Details in einem <a href="{CAL}">kurzen 15-Minuten-Gespräch</a>. Sie zahlen die Hälfte im Voraus und schicken Logo, Fotos und Texte.',
        "s3t": "Umsetzung",
        "s3d": "Die Website ist in etwa einer Woche fertig. Sie prüfen sie und wünschen Änderungen, bis Sie zufrieden sind.",
        "s4t": "Veröffentlichung",
        "s4d": "Sie zahlen den Rest, und die Website geht auf Ihrer Domain online. Für Änderungen bin ich jederzeit erreichbar.",
        "prices_h2": "Preise",
        "prices_intro": "Klar und im Voraus. Den genauen Preis vereinbaren wir nach dem Entwurf, je nachdem, wie viele Seiten und Funktionen Sie brauchen.",
        "p1h": "Neue Website",
        "p1amount": "ab 350 €",
        "p1unit": "einmalig",
        "p1note": "Die Hälfte im Voraus, der Rest bei Fertigstellung.",
        "p1a": "Design für Ihr Unternehmen",
        "p1b": "Optimiert für Smartphones und Google",
        "p1c": "Formular für Reservierungen oder Anfragen",
        "p1d": "Einrichtung auf Ihrer Domain",
        "p2h": "Hosting und Wartung",
        "p2unit": "pro Monat",
        "p2note": "Optional, aber so müssen Sie sich um nichts kümmern.",
        "p2a": "Schnelles, sicheres Hosting",
        "p2b": "Änderungen an Preisen, Fotos und Texten",
        "p2c": "Regelmäßige Kontrolle, dass alles funktioniert",
        "contact_h2": "Schauen wir uns Ihre Website an",
        "contact_p": "Schicken Sie mir die Adresse Ihrer Website oder einfach den Namen Ihres Unternehmens. Ich melde mich mit einem kostenlosen Entwurf für eine neue Startseite, und Sie entscheiden, ob Sie weitermachen möchten. Manuel Stanković, Fresh Front",
    },
    "ru": {
        "title": "Fresh Front – сайты для бизнеса по всей Хорватии",
        "description": "Современные сайты для малого бизнеса по всей Хорватии: удобные на телефоне, заметные в Google, с онлайн-бронированием. Бесплатный макет без обязательств.",
        "og_description": "Новый сайт для вашего бизнеса примерно за неделю. Бесплатный макет без обязательств.",
        "lang_nav_label": "Выберите язык",
        "brand_sub": "сайты",
        "nav_inquiry": "Отправить запрос",
        "subj_inquiry": "Запрос о сайте",
        "subj_concept": "Бесплатный макет сайта",
        "h1": "Новый сайт для вашего бизнеса, готовый за неделю.",
        "lead": "Я делаю сайты для ресторанов, автосервисов, клиник, салонов и малого бизнеса по всей Хорватии. Ещё до договорённости вы получаете бесплатный макет и видите, что именно получите.",
        "cta_concept": "Получить бесплатный макет",
        "cta_prices": "Посмотреть цены",
        "cta_call": "Записаться на звонок 15 мин",
        "compare_label": "Сравнение старого и нового сайта на телефоне",
        "old_bar": "KONOBA MUL - ДОБРО ПОЖАЛОВАТЬ НА НАШ САЙТ",
        "old_nav": "Главная | О нас | Блюда | Галерея | Контакты | Ссылки",
        "old_body": "Добро пожаловать в коноба Mul. Мы находимся у моря, в тихой бухте. Предлагаем домашнюю кухню, рыбу, мясо на гриле и домашние десерты. Наши блюда смотрите в меню выше.",
        "old_price": "Цены: рыбное ассорти 165,76 kn / 22,00 €",
        "old_notice": "Бронирование только по телефону!",
        "old_foot": "© 2017 Konoba Mul | Все права защищены",
        "tag_before": "До",
        "tag_after": "После",
        "new_sub": "Рыба, гриль и домашние десерты у моря",
        "new_meta": "Сегодня открыто 12–23<br>Меню с ценами в евро",
        "new_cta": "Забронировать столик",
        "new_cta2": "Позвонить",
        "demo_note": "Пример для вымышленного ресторана, как он выглядит на телефоне.",
        "gets_h2": "Что получает ваш бизнес",
        "gets_intro": "Большинство гостей и клиентов ищут вас с телефона. Сайт должен быстро показать, кто вы, что предлагаете и как с вами связаться.",
        "g1t": "Хорошо выглядит на телефоне",
        "g1d": "Текст читается без увеличения, а кнопки звонка и бронирования всегда под рукой.",
        "g2t": "Вас находят в Google",
        "g2d": "Сайт правильно настроен для поиска: адрес, часы работы и род деятельности.",
        "g3t": "Бронирование и заявки онлайн",
        "g3d": "Гости бронируют столик, клиенты записываются на услугу или приём, даже когда вы не можете ответить на звонок.",
        "g4t": "Актуальные цены и информация",
        "g4d": "Меню, прайс-лист и часы работы в евро и на нужных вам языках, всегда точные.",
        "g5t": "Изменения без хлопот",
        "g5d": "Напишите мне, что нужно поменять, и всё будет сделано. Никаких программ осваивать не нужно.",
        "g6t": "Хостинг и домен под контролем",
        "g6d": "Сайт быстрый и защищённый (https), а я слежу, чтобы всё работало.",
        "steps_h2": "Как это происходит",
        "steps_intro": "Вы ничего не платите, пока не увидите, как будет выглядеть ваш новый сайт.",
        "s1t": "Бесплатный макет",
        "s1d": "Напишите мне, и через день-два вы получите вариант главной страницы для вашего бизнеса, без обязательств.",
        "s2t": "Договорённость",
        "s2d": f'Если вам нравится, обсуждаем детали в <a href="{CAL}">коротком звонке на 15 минут</a>. Вы платите половину вперёд и присылаете логотип, фото и тексты.',
        "s3t": "Разработка",
        "s3d": "Сайт готов примерно за неделю. Вы его проверяете и просите правки, пока всё не устроит.",
        "s4t": "Запуск",
        "s4d": "Вы оплачиваете остаток, и сайт начинает работать на вашем домене. Для изменений я всегда на связи.",
        "prices_h2": "Цены",
        "prices_intro": "Понятно и заранее. Точную цену согласуем после макета, в зависимости от количества страниц и функций.",
        "p1h": "Новый сайт",
        "p1amount": "от 350 €",
        "p1unit": "разово",
        "p1note": "Половина вперёд, остаток после готовности сайта.",
        "p1a": "Дизайн под ваш бизнес",
        "p1b": "Удобно на телефоне и заметно в Google",
        "p1c": "Форма бронирования или заявки",
        "p1d": "Настройка на вашем домене",
        "p2h": "Хостинг и поддержка",
        "p2unit": "в месяц",
        "p2note": "Не обязательно, но тогда вам не о чем беспокоиться.",
        "p2a": "Быстрый и надёжный хостинг",
        "p2b": "Изменения цен, фото и текста",
        "p2c": "Регулярная проверка работы сайта",
        "contact_h2": "Давайте посмотрим ваш сайт",
        "contact_p": "Пришлите адрес вашего сайта или просто название бизнеса. Я пришлю бесплатный макет новой главной страницы, а вы решите, продолжать ли. Manuel Stanković, Fresh Front",
    },
    "es": {
        "title": "Fresh Front – páginas web para negocios en toda Croacia",
        "description": "Páginas web modernas para pequeños negocios en toda Croacia: adaptadas al móvil, fáciles de encontrar en Google, con reservas online. Diseño previo gratis y sin compromiso.",
        "og_description": "Una nueva página web para su negocio en una semana aproximadamente. Diseño previo gratis y sin compromiso.",
        "lang_nav_label": "Elija un idioma",
        "brand_sub": "páginas web",
        "nav_inquiry": "Enviar consulta",
        "subj_inquiry": "Consulta sobre página web",
        "subj_concept": "Diseño previo gratis",
        "h1": "Una nueva página web para su negocio, lista en una semana.",
        "lead": "Hago páginas web para restaurantes, talleres, clínicas, salones y pequeños negocios en toda Croacia. Antes de acordar nada, recibe un diseño previo gratis y ve exactamente lo que va a obtener.",
        "cta_concept": "Pedir diseño previo gratis",
        "cta_prices": "Ver precios",
        "cta_call": "Reservar llamada de 15 min",
        "compare_label": "Comparación de una página web antigua y una nueva en el móvil",
        "old_bar": "KONOBA MUL - BIENVENIDOS A NUESTRA PÁGINA WEB",
        "old_nav": "Inicio | Nosotros | Especialidades | Galería | Contacto | Enlaces",
        "old_body": "Bienvenidos a la Konoba Mul. Estamos junto al mar, en una cala tranquila. Ofrecemos cocina casera, pescado, carne a la parrilla y postres caseros. Vea nuestras especialidades en el menú de arriba.",
        "old_price": "Precios: tabla de pescado 165,76 kn / 22,00 €",
        "old_notice": "¡Reservas solo por teléfono!",
        "old_foot": "© 2017 Konoba Mul | Todos los derechos reservados",
        "tag_before": "Antes",
        "tag_after": "Después",
        "new_sub": "Pescado, parrilla y postres caseros junto al mar",
        "new_meta": "Abierto hoy 12–23 h<br>Carta con precios en euros",
        "new_cta": "Reservar mesa",
        "new_cta2": "Llámenos",
        "demo_note": "Ejemplo de un restaurante inventado, tal como se ve en el móvil.",
        "gets_h2": "Qué recibe su negocio",
        "gets_intro": "La mayoría de sus clientes le buscan desde el móvil. Su página web debe decir rápido quién es, qué ofrece y cómo contactarle.",
        "g1t": "Se ve bien en el móvil",
        "g1d": "El texto se lee sin hacer zoom y los botones para llamar y reservar están siempre a mano.",
        "g2t": "Le encuentran en Google",
        "g2d": "La página está bien configurada para buscadores, con su dirección, horario y actividad.",
        "g3t": "Reservas y consultas online",
        "g3d": "Los clientes reservan mesa o piden cita aunque usted no pueda atender el teléfono.",
        "g4t": "Precios e información al día",
        "g4d": "Carta, lista de precios y horario en euros y en los idiomas que necesite, siempre correctos.",
        "g5t": "Cambios sin complicaciones",
        "g5d": "Me envía un mensaje con lo que hay que cambiar y queda hecho. Sin aprender ningún programa.",
        "g6t": "Alojamiento y dominio resueltos",
        "g6d": "La página es rápida y segura (https), y yo me encargo de que todo funcione.",
        "steps_h2": "Cómo funciona",
        "steps_intro": "No paga nada hasta ver cómo quedaría su nueva página web.",
        "s1t": "Diseño previo gratis",
        "s1d": "Escríbame y en uno o dos días recibe una propuesta de página de inicio para su negocio, sin compromiso.",
        "s2t": "Acuerdo",
        "s2d": f'Si le gusta, concretamos los detalles en una <a href="{CAL}">breve llamada de 15 minutos</a>. Paga la mitad por adelantado y envía su logo, fotos y textos.',
        "s3t": "Desarrollo",
        "s3d": "La página está lista en una semana aproximadamente. La revisa y pide cambios hasta quedar satisfecho.",
        "s4t": "Publicación",
        "s4d": "Paga el resto y la página se publica en su dominio. Para cambios, siempre estoy disponible.",
        "prices_h2": "Precios",
        "prices_intro": "Claros y por adelantado. El precio exacto lo acordamos después del diseño previo, según cuántas páginas y funciones necesite.",
        "p1h": "Nueva página web",
        "p1amount": "desde 350 €",
        "p1unit": "pago único",
        "p1note": "La mitad por adelantado, el resto al terminar la página.",
        "p1a": "Diseño a medida de su negocio",
        "p1b": "Adaptada al móvil y a Google",
        "p1c": "Formulario de reservas o consultas",
        "p1d": "Configuración en su propio dominio",
        "p2h": "Alojamiento y mantenimiento",
        "p2unit": "al mes",
        "p2note": "Opcional, pero así no tiene que preocuparse de nada.",
        "p2a": "Alojamiento rápido y seguro",
        "p2b": "Cambios de precios, fotos y textos",
        "p2c": "Revisión de que todo funciona",
        "contact_h2": "Veamos su página web",
        "contact_p": "Envíeme la dirección de su página o simplemente el nombre de su negocio. Le responderé con un diseño previo gratis de una nueva página de inicio, y usted decide si seguimos. Manuel Stanković, Fresh Front",
    },
}


def flags_html(current):
    out = []
    for code in LANGS:
        cur = ' aria-current="true"' if code == current else ""
        out.append(
            f'  <a href="{PATHS[code]}" hreflang="{code}" lang="{code}" title="{NAMES[code]}"'
            f' aria-label="{NAMES[code]}"{cur}>{FLAGS[code]}</a>'
        )
    return "\n".join(out)


def alternates_html():
    lines = [f'<link rel="alternate" hreflang="{c}" href="{SITE}{PATHS[c]}">' for c in LANGS]
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/">')
    return "\n".join(lines)


def build():
    template = open(os.path.join(ROOT, "src", "template.html"), encoding="utf-8").read()
    style = open(os.path.join(ROOT, "src", "style.html"), encoding="utf-8").read().strip()
    keys = set(re.findall(r"\{\{(\w+)\}\}", template))
    for code in LANGS:
        t = dict(T[code])
        missing = keys - set(t) - {
            "lang", "url", "alternates", "font_url", "font_display", "font_body", "style", "flags", "home",
        }
        missing -= {k for k in keys if k.startswith("subj_")} - set(t)
        assert not missing, (code, sorted(missing))
        fonts = CYRILLIC_FONTS if code == "ru" else LATIN_FONTS
        t.update({
            "lang": code,
            "url": SITE + PATHS[code],
            "alternates": alternates_html(),
            "font_url": fonts[0].replace("&", "&amp;"),
            "font_display": fonts[1],
            "font_body": fonts[2],
            "style": style,
            "flags": flags_html(code),
            "home": PATHS[code],
        })
        t["subj_inquiry"] = quote(T[code]["subj_inquiry"])
        t["subj_concept"] = quote(T[code]["subj_concept"])
        html = re.sub(r"\{\{(\w+)\}\}", lambda m: t[m.group(1)], template)
        out_dir = ROOT if code == "hr" else os.path.join(ROOT, code)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print("built", code)


if __name__ == "__main__":
    build()
