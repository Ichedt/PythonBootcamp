# Day 1 - Band Name Generator
#
# tags: string, print, input, variables

print("Welcome to the Band Name Generator!")

print("Which city did you grow up in?")
city = input()

print("Choose a pet name.")
pet = input()

band_name = city + " " + pet + "s"
print(f"Your band name is: {band_name}.")

# NOTES
# Name convention: Google Python Style Guide suggests the following convention for naming things:
# module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name, local_var_name, CLASS_CONSTANT_NAME.
