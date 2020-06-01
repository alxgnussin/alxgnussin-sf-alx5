from random import sample

from models import Category, Meal


def get_meals_for_main(db):
    categories = db.session.query(Category).order_by('id').all()
    meals = db.session.query(Meal).all()
    meal_objects = []
    for x in categories:
        meals_list = []
        for y in meals:
            if x.id == y.category_id:
                meals_list.append(y)
        meals_random = sample(meals_list, 3)
        my_dict = {'category_title': x.title, 'meals': meals_random}
        meal_objects.append(my_dict)
    return meal_objects
