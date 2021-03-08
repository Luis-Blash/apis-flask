from flask import  Flask,jsonify,request
from http import HTTPStatus

app = Flask(__name__)

# mis recipiente
recipes = [
    {
        'id': 1,
        'name': 'Egg Salad',
        'description': 'This is a lovely egg salad recipe.'
    },
    {
        'id': 2,
        'name': 'Tomato Pasta',
        'description': 'This is a lovely tomato pasta recipe.'
    }
]

# este es en general recetas, recibo todas las recetas
@app.route('/recipes/', methods=['GET'])
def get_recipes():
    # un json que como titulo dice data, pero viene de mi codigo
    return jsonify({'data': recipes})

# solo uno, me devuelve uno por id
@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    # solo saca la id de mi diccionario
    recipe = next((
        recipe
        for recipe in recipes
            if recipe['id'] == recipe_id),
        None)
    print(recipe)
    if recipe:
        return jsonify(recipe)
    # en caso no existir mandar un not found
    return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND

# para crear uno nuevo
@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    # como es una lista dentro tiene un diccionarios, guarda un nuevo dato
    recipe = {
        'id': len(recipes) + 1,
        'name': name,
        'description': description
    }
    recipes.append(recipe)
    return jsonify(recipe), HTTPStatus.CREATED

@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)
    if not recipe:
        return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND
    data = request.get_json()
    recipe.update(
        {
            'name': data.get('name'),
            'description': data.get('description')
        }
    )
    return jsonify(recipe)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")