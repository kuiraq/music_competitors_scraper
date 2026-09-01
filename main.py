from google_play_scraper import reviews, Sort

app_id = 'com.spotify.music'  
result, continuation_token = reviews(
    app_id,
    lang='ru',  
    country='ru',  
    sort=Sort.NEWEST,  
    count=1500,  
   
)
for review in result:
    print("Оценка:", review['score'])
    print("Текст:", review['content'])
    print("-" * 40)

keywords = ["шаффл", "шафл", "перемешив", "повторя", "рандом", "одни и те же"]

bad_reviews = []
suffle_issues=[]
for review in result:
    score = review['score']
    content = review['content'].lower()
    if not content:
        continue
    if score <= 3:
        bad_reviews.append(review)
        if any(keyword in content for keyword in keywords):
            suffle_issues.append(review)

total_parsed = len(result)
total_bad_reviews = len(bad_reviews)
total_suffle_issues = len(suffle_issues)

print(f"Всего спарсили отзывов: {total_parsed}")
print(f"Из них негативных (1-3 звезды): {total_bad_reviews}")
print(f"Из них с жалобами на алгоритм: {total_suffle_issues}")

if total_bad_reviews > 0:
    percentage_bad_reviews = (total_bad_reviews / total_parsed) * 100
    print(f"Процент негативных отзывов: {percentage_bad_reviews:.2f}%")
    print(f"\nаргумент:")
    print(f"Из {total_bad_reviews} последних негативных отзывов {percentage_bad_reviews:.1f}% жалуются на алгоритм шаффла.")