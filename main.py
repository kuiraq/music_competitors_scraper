import csv
from google_play_scraper import reviews, Sort

apps = {
    "Spotify": "com.spotify.music",
    'Яндекс Музыка': 'ru.yandex.music',
    'VK Музыка': 'com.vkontakte.android',
}

keywords = ["шаффл", "шафл", "перемешив", "повторя", "рандом", "одни и те же"]

output_file = "reviews.csv"
with open(output_file, "w", encoding="utf-8-sig", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Сервис', 'Дата', 'Оценка', 'Текст отзыва', 'Ключевые слова'])
    print('Парсим отзывы с Google Play...')
    for app_name, app_id in apps.items():
        try:
            result, _ = reviews(
            app_id,
            lang='ru',
            country='ru',
            sort=Sort.NEWEST,
            count=1500
            )
        except Exception as e:
            print(f"Ошибка при парсинге отзывов для {app_name}: {e}")
            continue
        bad_revies_count=0
        shuffle_reviews=[]
        for review in result:
            score = review['score']
            raw_content=review.get('content')
            if not raw_content:
                continue
            content = raw_content.lower()
            date = review['at'].strftime('%Y-%m-%d %H:%M') if review.get('at') else ''
            if not content:
                continue
            if score <= 3:
                bad_revies_count += 1
                matched_keywords = [keyword for keyword in keywords if keyword in content]
                if matched_keywords:
                    shuffle_reviews.append(review)
                    writer.writerow([
                        app_name, date, score, content.strip().replace('\n', ' '), ', '.join(matched_keywords)
                    ])


        total_parsed = len(result)
        total_shuffle=len(shuffle_reviews)

        print(f"Всего спарсили отзывов: {total_parsed}")
        print(f"Из них негативных (1-3 звезды): {bad_revies_count}")
        print(f"Из них с жалобами на алгоритм: {total_shuffle}")

        if bad_revies_count > 0:
            percentage = (total_shuffle / bad_revies_count) * 100
            print(f"Процент негативных отзывов с жалобами на алгоритм: {percentage:.2f}%")
        else:
            print("Нет негативных отзывов для анализа.")

print(f"Результаты сохранены в файл: {output_file}")