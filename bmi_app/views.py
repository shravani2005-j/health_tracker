from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# -------------------- User Registration --------------------
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'bmi_app/register.html')


# -------------------- User Login --------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('bmi_input')
        else:
            messages.error(request, "Invalid credentials!")

    return render(request, 'bmi_app/login.html')


# -------------------- BMI Input --------------------
def bmi_input_view(request):
    return render(request, 'bmi_app/bmi_input.html')


# -------------------- BMI Result --------------------
def bmi_result_view(request):
    bmi = None
    category = None
    diet_type = None
    diet = {}

    if request.method == "POST":
        try:
            weight = float(request.POST.get('weight'))
            height = float(request.POST.get('height')) / 100
            bmi = round(weight / (height * height), 2)
            diet_type = request.POST.get('diet_type')  # veg or nonveg

            # Determine BMI category
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 24.9:
                category = "Normal weight"
            elif 25 <= bmi < 29.9:
                category = "Overweight"
            else:
                category = "Obese"

            # Full Diet Plans
            diet_plans = {
                "Underweight": {
                    "veg": {
                        "Breakfast": "Oatmeal with milk, banana, nuts, honey",
                        "Mid-morning Snack": "Smoothie with yogurt, peanut butter, fruits",
                        "Lunch": "Brown rice, paneer, lentils, vegetables",
                        "Afternoon Snack": "Nuts, seeds, avocado toast",
                        "Dinner": "Whole wheat pasta with vegetables and tofu",
                        "Before Bed": "Warm milk or yogurt"
                    },
                    "nonveg": {
                        "Breakfast": "Oatmeal with milk, banana, nuts, honey",
                        "Mid-morning Snack": "Smoothie with yogurt, peanut butter, fruits",
                        "Lunch": "Brown rice, grilled chicken/fish, vegetables",
                        "Afternoon Snack": "Nuts, seeds, boiled eggs",
                        "Dinner": "Whole wheat pasta with chicken/fish and vegetables",
                        "Before Bed": "Warm milk"
                    }
                },
                "Normal weight": {
                    "veg": {
                        "Breakfast": "Whole-grain toast, eggs or tofu scramble, fruit",
                        "Mid-morning Snack": "Fruit or nuts",
                        "Lunch": "Quinoa, lentils, vegetables, salad",
                        "Afternoon Snack": "Yogurt or nuts",
                        "Dinner": "Grilled tofu, vegetables, small portion of brown rice",
                        "Evening": "Herbal tea or water"
                    },
                    "nonveg": {
                        "Breakfast": "Whole-grain toast, boiled eggs, fruit",
                        "Mid-morning Snack": "Fruit or nuts",
                        "Lunch": "Quinoa, grilled chicken/fish, vegetables",
                        "Afternoon Snack": "Yogurt or boiled eggs",
                        "Dinner": "Grilled fish/chicken, vegetables, small portion of rice",
                        "Evening": "Herbal tea or water"
                    }
                },
                "Overweight": {
                    "veg": {
                        "Breakfast": "Oatmeal with skimmed milk, berries",
                        "Mid-morning Snack": "Fresh fruit",
                        "Lunch": "Large salad with lentils/beans, small portion of grains",
                        "Afternoon Snack": "Carrot/cucumber sticks or nuts",
                        "Dinner": "Steamed vegetables, grilled paneer/tofu, small portion of carbs",
                        "Evening": "Water or herbal tea"
                    },
                    "nonveg": {
                        "Breakfast": "Oatmeal with skimmed milk, berries",
                        "Mid-morning Snack": "Fresh fruit",
                        "Lunch": "Salad with grilled chicken/fish, small portion of grains",
                        "Afternoon Snack": "Carrot/cucumber sticks or boiled eggs",
                        "Dinner": "Steamed vegetables, grilled fish/chicken, very small portion of carbs",
                        "Evening": "Water or herbal tea"
                    }
                },
                "Obese": {
                    "veg": {
                        "Breakfast": "Vegetable omelette or tofu scramble",
                        "Mid-morning Snack": "Fresh fruit (avoid high sugar fruits)",
                        "Lunch": "Large salad with legumes/protein, minimal carbs",
                        "Afternoon Snack": "Cucumber/carrot sticks",
                        "Dinner": "Steamed vegetables, tofu, minimal carbs",
                        "Evening": "Warm water or herbal tea"
                    },
                    "nonveg": {
                        "Breakfast": "Vegetable omelette or boiled eggs",
                        "Mid-morning Snack": "Fresh fruit (avoid high sugar fruits)",
                        "Lunch": "Large salad with grilled chicken/fish, minimal carbs",
                        "Afternoon Snack": "Cucumber/carrot sticks or boiled eggs",
                        "Dinner": "Steamed vegetables, grilled fish/chicken, minimal carbs",
                        "Evening": "Warm water or herbal tea"
                    }
                }
            }

            diet = diet_plans.get(category, {}).get(diet_type, {"Message": "No diet plan available."})

        except:
            bmi = None
            category = "Invalid input"

    return render(request, 'bmi_app/bmi_result.html', {
        'bmi': bmi,
        'category': category,
        'diet_type': diet_type,
        'diet': diet
    })


# -------------------- Download BMI & Diet Plan --------------------
def download_bmi_diet(request):
    bmi = request.GET.get('bmi')
    category = request.GET.get('category')
    diet_type = request.GET.get('diet_type')

    # Same diet plans as above
    diet_plans = {
        "Underweight": {
            "veg": {
                "Breakfast": "Oatmeal with milk, banana, nuts, honey",
                "Mid-morning Snack": "Smoothie with yogurt, peanut butter, fruits",
                "Lunch": "Brown rice, paneer, lentils, vegetables",
                "Afternoon Snack": "Nuts, seeds, avocado toast",
                "Dinner": "Whole wheat pasta with vegetables and tofu",
                "Before Bed": "Warm milk or yogurt"
            },
            "nonveg": {
                "Breakfast": "Oatmeal with milk, banana, nuts, honey",
                "Mid-morning Snack": "Smoothie with yogurt, peanut butter, fruits",
                "Lunch": "Brown rice, grilled chicken/fish, vegetables",
                "Afternoon Snack": "Nuts, seeds, boiled eggs",
                "Dinner": "Whole wheat pasta with chicken/fish and vegetables",
                "Before Bed": "Warm milk"
            }
        },
        "Normal weight": {
            "veg": {
                "Breakfast": "Whole-grain toast, eggs or tofu scramble, fruit",
                "Mid-morning Snack": "Fruit or nuts",
                "Lunch": "Quinoa, lentils, vegetables, salad",
                "Afternoon Snack": "Yogurt or nuts",
                "Dinner": "Grilled tofu, vegetables, small portion of brown rice",
                "Evening": "Herbal tea or water"
            },
            "nonveg": {
                "Breakfast": "Whole-grain toast, boiled eggs, fruit",
                "Mid-morning Snack": "Fruit or nuts",
                "Lunch": "Quinoa, grilled chicken/fish, vegetables",
                "Afternoon Snack": "Yogurt or boiled eggs",
                "Dinner": "Grilled fish/chicken, vegetables, small portion of rice",
                "Evening": "Herbal tea or water"
            }
        },
        "Overweight": {
            "veg": {
                "Breakfast": "Oatmeal with skimmed milk, berries",
                "Mid-morning Snack": "Fresh fruit",
                "Lunch": "Large salad with lentils/beans, small portion of grains",
                "Afternoon Snack": "Carrot/cucumber sticks or nuts",
                "Dinner": "Steamed vegetables, grilled paneer/tofu, small portion of carbs",
                "Evening": "Water or herbal tea"
            },
            "nonveg": {
                "Breakfast": "Oatmeal with skimmed milk, berries",
                "Mid-morning Snack": "Fresh fruit",
                "Lunch": "Salad with grilled chicken/fish, small portion of grains",
                "Afternoon Snack": "Carrot/cucumber sticks or boiled eggs",
                "Dinner": "Steamed vegetables, grilled fish/chicken, very small portion of carbs",
                "Evening": "Water or herbal tea"
            }
        },
        "Obese": {
            "veg": {
                "Breakfast": "Vegetable omelette or tofu scramble",
                "Mid-morning Snack": "Fresh fruit (avoid high sugar fruits)",
                "Lunch": "Large salad with legumes/protein, minimal carbs",
                "Afternoon Snack": "Cucumber/carrot sticks",
                "Dinner": "Steamed vegetables, tofu, minimal carbs",
                "Evening": "Warm water or herbal tea"
                },
            "nonveg": {
                "Breakfast": "Vegetable omelette or boiled eggs",
                "Mid-morning Snack": "Fresh fruit (avoid high sugar fruits)",
                "Lunch": "Large salad with grilled chicken/fish, minimal carbs",
                "Afternoon Snack": "Cucumber/carrot sticks or boiled eggs",
                "Dinner": "Steamed vegetables, grilled fish/chicken, minimal carbs",
                "Evening": "Warm water or herbal tea"
            }
        }
    }
    diet = diet_plans.get(category, {}).get(diet_type)
    
    
    if not diet:
        diet = {"Message": "No diet plan available."}

   
    content = f"BMI: {bmi}\nCategory: {category}\nDiet Type: {diet_type}\n\nDiet Plan:\n"
    for meal, plan in diet.items():
        content += f"{meal}: {plan}\n"

   
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=BMI_{category}_{diet_type}.txt'
    return response