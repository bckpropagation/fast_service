from flask_restplus import Namespace, fields


class MenuDto:
	api = Namespace(
		"menu",
		description="Information of restaurant menu"
	)

	min_model = {
		"id": fields.Integer(
			description="Dish id"
		),
		"name": fields.String(
			description="Dish name"
		),
		"type": fields.String(
			description="Dish type"
		)
	}

	menu = api.model(
		"menu",
		min_model
	)

	full_model = min_model
	full_model["description"] = fields.String(
		description="Dish description"
	)
	dish = api.model(
		"dish",
		full_model
	)


class RestaurantsDto:
	api = Namespace(
		"restaurants",
		description="Information of registered restaurants."
	)

	min_model = {
		"id": fields.Integer(
			description="Restaurant id number"
		),
		"name": fields.String(
			description="Restaurant name"
		),
		"hours": fields.String(
			description="Restaurant work hours"
		)
	}

	minified_restaurant = api.model(
		"resturants",
		min_model
	)
	
	full_model = min_model
	full_model["menus"] = fields.List(
		fields.Nested(MenuDto.menu)
	)

	restaurant = api.model(
		"restaurant",
		full_model
	)
