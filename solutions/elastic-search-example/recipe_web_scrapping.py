# https://www.allrecipes.com/recipes/
import json
from time import sleep

import requests
from bs4 import BeautifulSoup
import elasticsearchstartup


def parse(u):
    print(u)
    title = '-'
    submit_by = '-'
    description = '-'
    calories = 0
    preperation_time = '-'
    ingredients = []
    preperation_steps = []
    rec = {}
    try:
        r = requests.get(u, headers=headers)
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            title_section = soup.select('.recipe-summary__h1')
            submitter_section = soup.select('.submitter__name')
            description_section = soup.select('.submitter__description')
            ingredients_section = soup.select('.recipe-ingred_txt')
            calories_section = soup.select('.calorie-count')
            directionsList = soup.select(".recipe-directions__list--item")
            prep_time_list = soup.select(".ready-in-time")
            if calories_section:
                calories = calories_section[0].text.replace('cals', '').strip()
            if ingredients_section:
                for ingredient in ingredients_section:
                    ingredient_text = ingredient.text.strip()
                    if 'Add all ingredients to list' not in ingredient_text and ingredient_text != '':
                        ingredients.append({'step': ingredient.text.strip()})
            if description_section:
                description = description_section[0].text.strip().replace('"', '')
            if submitter_section:
                submit_by = submitter_section[0].text.strip()
            if title_section:
                title = title_section[0].text
            if directionsList:
                for direction in directionsList:
                    direction_text = direction.text.strip()
                    if direction_text != '':
                        preperation_steps.append(direction_text)
            if prep_time_list:
                for prep_time in prep_time_list:
                    preperation_time = prep_time.text
            rec = {'title': title, 'submitter': submit_by, 'description': description, 'calories': calories,
                   'ingredients': ingredients, "directions": preperation_steps, "ready_in": preperation_time}
    except Exception as ex:
        print("got exception", ex)
        print(ex)
    finally:
        return json.dumps(rec)


if __name__ == '__main__':
    elasticsearchstartup.main()
    es = elasticsearchstartup.es_object
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Pragma': 'no-cache'
    }
    url = 'https://www.allrecipes.com/recipes/96/salad/'
    # r = requests.get(url, headers=headers)
    # if r.status_code == 200:
    #     html = r.text
    #     soup = BeautifulSoup(html, 'lxml')
    #     links = soup.select('.fixed-recipe-card__h3 a')
    #     const = "salad"
    #     index = 0
    #     for link in links:
    #         sleep(4)
    #         index = index + 1
    #         result = parse(link['href'])
    #         print(result)
    #         elasticsearchstartup.store_record(es, record=result, id=const + str(index))
    #         print("=============================================================")
    # search_object = {'query': {'match': {'calories': '102'}}}
    search_object = {'_source': ['calories'], 'query': {'range': {'calories': {'gte': 500}}}}
    s_data = elasticsearchstartup.search(es, json.dumps(search_object))
    print(s_data)
